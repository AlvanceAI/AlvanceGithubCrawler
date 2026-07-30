#!/usr/bin/env bash
set -Eeuo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

publish_branch=${PUBLISH_BRANCH:-XBY}
per_key_concurrency=${E2B_CONCURRENCY:-20}
prescreen_concurrency=${PRESCREEN_CONCURRENCY:-20}
package_repair_workers=${PACKAGE_REPAIR_WORKERS:-8}
batch_per_language=${BATCH_PER_LANGUAGE:-100}
max_per_language=${MAX_PER_LANGUAGE:-1000}
run_id=${PIPELINE_RUN_ID:-github-mass-production-$(date -u +%Y%m%dT%H%M%SZ)}
run_root=${PIPELINE_RUN_ROOT:-outputs/production-runs}
run_dir="$run_root/$run_id"
crawl_dir=${CRAWL_OUTPUT_DIR:-outputs/github_crawl_500_unquota}
production_dir=${PRODUCTION_OUTPUT_DIR:-outputs/github_production_500_unquota}
log_dir="$run_dir/logs"
timings_path="$run_dir/stage-timings.jsonl"
producer_done="$run_dir/producer.done"
producer_status="$run_dir/producer.status"
keys_exhausted="$run_dir/e2b-keys-exhausted"
report_doc="docs/continuous-production-$run_id.md"
publish_tasks=${PUBLISH_TASKS:-true}
publish_run_artifacts=${PUBLISH_RUN_ARTIFACTS:-true}
producer_pid=""

for command_name in git jq uv; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "missing required command: $command_name" >&2
        exit 2
    fi
done

if [[ ! $run_id =~ ^[A-Za-z0-9._-]+$ ]]; then
    echo "PIPELINE_RUN_ID may contain only letters, digits, dot, underscore, and hyphen" >&2
    exit 2
fi
if (( per_key_concurrency < 1 || per_key_concurrency > 20 )); then
    echo "E2B_CONCURRENCY must be between 1 and 20 per key" >&2
    exit 2
fi
if (( prescreen_concurrency < 1 || prescreen_concurrency > 20 )); then
    echo "PRESCREEN_CONCURRENCY must be between 1 and 20" >&2
    exit 2
fi
if (( package_repair_workers < 1 || package_repair_workers > 20 )); then
    echo "PACKAGE_REPAIR_WORKERS must be between 1 and 20" >&2
    exit 2
fi
if (( batch_per_language < 1 || max_per_language < 1 )); then
    echo "BATCH_PER_LANGUAGE and MAX_PER_LANGUAGE must be positive" >&2
    exit 2
fi
if [[ $(git branch --show-current) != "$publish_branch" ]]; then
    echo "continuous production must run on branch $publish_branch" >&2
    exit 2
fi

mkdir -p "$crawl_dir" "$production_dir" "$log_dir"
rm -f "$producer_done" "$producer_status" "$keys_exhausted"

run_stage() {
    local stage=$1
    shift
    local log_path="$log_dir/$stage.log"
    local started_at started_epoch finished_at finished_epoch status duration
    local restore_errexit=false
    [[ $- == *e* ]] && restore_errexit=true
    started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    started_epoch=$(date +%s)

    set +e
    {
        echo "[$started_at] stage=$stage run_id=$run_id"
        printf 'command='
        printf ' %q' "$@"
        printf '\n'
        "$@"
    } 2>&1 | tee -a "$log_path"
    status=${PIPESTATUS[0]}
    if [[ $restore_errexit == true ]]; then
        set -e
    else
        set +e
    fi

    finished_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    finished_epoch=$(date +%s)
    duration=$((finished_epoch - started_epoch))
    printf \
        '{"run_id":"%s","stage":"%s","started_at":"%s","finished_at":"%s","duration_s":%d,"exit_code":%d}\n' \
        "$run_id" "$stage" "$started_at" "$finished_at" "$duration" "$status" \
        >> "$timings_path"
    echo "[$finished_at] stage=$stage exit_code=$status duration_s=$duration" \
        | tee -a "$log_path"
    return "$status"
}

pending_count() {
    uv run python -m alvance_github_crawler.run_report pending-count \
        "$production_dir/pending.jsonl"
}

write_report() {
    uv run python -m alvance_github_crawler.run_report build \
        --run-id "$run_id" \
        --crawl-dir "$crawl_dir" \
        --production-dir "$production_dir" \
        --timings "$timings_path" \
        --output-json "$run_dir/metrics.json" \
        --output-md "$run_dir/statistics.md" \
        >> "$log_dir/report.log" 2>&1 || true
    if [[ -f "$run_dir/statistics.md" ]]; then
        cp "$run_dir/statistics.md" "$report_doc"
    fi
}

publish_completed_tasks() {
    [[ $publish_tasks == true ]] || return 0
    git add -- catalog materials tasks
    if git diff --cached --quiet; then
        return 0
    fi
    git commit -m "chore(tasks): publish $run_id batch $(date -u +%Y%m%dT%H%M%SZ)"
    git push origin "$publish_branch"
}

publish_final_report() {
    [[ $publish_run_artifacts == true ]] || return 0
    git add -- "$crawl_dir" "$production_dir" "$run_dir" "$report_doc"
    if git diff --cached --quiet; then
        return 0
    fi
    git commit -m "docs: record $run_id production statistics"
    git push origin "$publish_branch"
}

current_per_language() {
    if [[ ! -f "$crawl_dir/raw_repositories.jsonl" ]]; then
        echo 0
        return
    fi
    jq -sr '
        reduce .[] as $repo (
            {};
            .[$repo._crawl.query_language // "unknown"] += 1
        )
        | [
            .python // 0,
            .go // 0,
            .typescript // 0,
            .javascript // 0,
            .rust // 0
        ]
        | min
    ' "$crawl_dir/raw_repositories.jsonl"
}

run_prescreen() {
    local stage=$1
    run_stage "$stage" \
        env \
            PIPELINE_OUTPUT_DIR="$production_dir" \
            PIPELINE_LANGUAGE_QUOTA_ENABLED=false \
            PIPELINE_PRESCREEN_CONCURRENCY="$prescreen_concurrency" \
            uv run alvance-github-crawler produce \
            --input "$crawl_dir/accepted_repositories.jsonl" \
            --prescreen-concurrency "$prescreen_concurrency" \
            --defer-e2b \
            --verbose
}

produce_candidates() {
    local current next target
    current=$(current_per_language)
    if (( current > 0 )); then
        run_prescreen "prescreen-resume-$((current * 5))" || return $?
    fi
    while (( current < max_per_language )); do
        next=$((current + batch_per_language))
        if (( next > max_per_language )); then
            next=$max_per_language
        fi
        target=$((next * 5))
        run_stage "crawl-$target" \
            uv run alvance-github-crawler crawl \
            --target-total "$target" \
            --per-language "$next" \
            --max-search-pages 10 \
            --output "$crawl_dir" \
            --request-interval 0.2 \
            --verbose || return $?
        run_prescreen "prescreen-$target" || return $?
        current=$next
    done
}

start_producer() {
    (
        set +e
        produce_candidates
        status=$?
        printf '%d\n' "$status" > "$producer_status"
        touch "$producer_done"
    ) &
    producer_pid=$!
}

stop_producer() {
    if [[ -n $producer_pid ]] && kill -0 "$producer_pid" 2>/dev/null; then
        kill -TERM "$producer_pid"
        wait "$producer_pid" 2>/dev/null || true
    fi
}

verify_once() {
    local tier=$1
    local cpu_count=$2
    local memory_mb=$3
    local status
    set +e
    run_stage "verify-$tier-$(date -u +%Y%m%dT%H%M%SZ)" \
        env \
            PIPELINE_OUTPUT_DIR="$production_dir" \
            PIPELINE_E2B_CPU_COUNT="$cpu_count" \
            PIPELINE_E2B_MEMORY_MB="$memory_mb" \
            PIPELINE_E2B_CONCURRENCY="$per_key_concurrency" \
            PIPELINE_LANGUAGE_QUOTA_ENABLED=false \
            uv run alvance-github-crawler \
            --verify-pending \
            --e2b-concurrency "$per_key_concurrency" \
            --verbose
    status=$?
    set -e
    publish_completed_tasks
    return "$status"
}

consume_until_idle() {
    local tier=$1
    local cpu_count=$2
    local memory_mb=$3
    local wait_for_producer=$4
    local before after status delay=15
    while true; do
        before=$(pending_count)
        if (( before == 0 )); then
            if [[ $wait_for_producer == true && ! -f $producer_done ]]; then
                sleep 10
                continue
            fi
            return 0
        fi

        set +e
        verify_once "$tier" "$cpu_count" "$memory_mb"
        status=$?
        set -e
        if (( status == 4 )); then
            touch "$keys_exhausted"
            return 4
        fi
        after=$(pending_count)
        if (( status != 0 || after >= before )); then
            echo "pending=$after tier=$tier; retrying after ${delay}s" \
                | tee -a "$log_dir/verify-$tier.log"
            sleep "$delay"
            delay=$((delay < 60 ? delay + 15 : 60))
        else
            delay=15
        fi
    done
}

cleanup() {
    stop_producer
    write_report
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

doctor_json=$(
    PIPELINE_E2B_CONCURRENCY="$per_key_concurrency" \
    PIPELINE_PRESCREEN_CONCURRENCY="$prescreen_concurrency" \
        uv run alvance-github-crawler --doctor
)
github_ready=$(jq -r '.github_token // false' <<< "$doctor_json")
openai_ready=$(jq -r '.openai_api_key // false' <<< "$doctor_json")
openai_sdk_ready=$(jq -r '.openai_sdk // false' <<< "$doctor_json")
e2b_sdk_ready=$(jq -r '.e2b_sdk // false' <<< "$doctor_json")
key_count=$(jq -r '.e2b_api_key_count // 0' <<< "$doctor_json")
total_concurrency=$(jq -r '.e2b_total_concurrency // 0' <<< "$doctor_json")

if [[ $github_ready != true ]]; then
    echo "missing GitHub credentials; set GITHUB_TOKEN in .env or authenticate gh" >&2
    exit 2
fi
if [[ $openai_ready != true ]]; then
    echo "missing model credentials; set OPENAI_API_KEY in .env" >&2
    exit 2
fi
if [[ $openai_sdk_ready != true || $e2b_sdk_ready != true ]]; then
    echo "missing Python dependencies; run: uv sync --extra e2b --extra dev" >&2
    exit 2
fi
if (( key_count != 2 || total_concurrency != per_key_concurrency * 2 )); then
    echo "expected E2B_API_KEY1 and E2B_API_KEY2 in .env and $((per_key_concurrency * 2)) total slots" >&2
    exit 2
fi
echo "preflight passed: branch=$publish_branch prescreen=$prescreen_concurrency e2b_keys=$key_count e2b_slots=$total_concurrency"

if [[ -s catalog/e2b-packages.jsonl ]]; then
    run_stage repair-rebuildable-packages \
        uv run python scripts/repair_rebuildable_tasks.py \
        --root "$repo_root" \
        --workers "$package_repair_workers"
fi

start_producer
set +e
consume_until_idle default 1 1024 true
consumer_status=$?
set -e

if (( consumer_status == 4 )); then
    stop_producer
else
    wait "$producer_pid" || true
    producer_pid=""
    producer_exit=$(cat "$producer_status")
    if (( producer_exit != 0 )); then
        echo "producer stopped with exit code $producer_exit; draining completed input" >&2
    fi

    run_stage requeue-resource-failures \
        env PIPELINE_OUTPUT_DIR="$production_dir" \
        uv run alvance-github-crawler \
        --requeue-failures \
        --failure-reason e2b_resource_exhausted \
        --failure-reason benchmark_resource_fail \
        --failure-reason offline_test_timeout \
        --verbose

    set +e
    consume_until_idle escalated 2 4096 false
    consumer_status=$?
    set -e
fi

write_report
publish_completed_tasks
publish_final_report
trap - EXIT INT TERM

if [[ -f $keys_exhausted ]]; then
    echo "continuous production stopped: both E2B key slots exhausted"
    exit 4
fi
echo "continuous production complete: $run_dir"
