#!/usr/bin/env bash
set -Eeuo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

target_total=${TARGET_TOTAL:-500}
per_language=${PER_LANGUAGE:-100}
e2b_concurrency=${E2B_CONCURRENCY:-20}
verify_rounds=${VERIFY_ROUNDS:-5}
run_id=${PIPELINE_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}
run_root=${PIPELINE_RUN_ROOT:-outputs/production-runs}
run_dir="$run_root/$run_id"
crawl_dir=${CRAWL_OUTPUT_DIR:-$run_dir/crawl}
production_dir=${PRODUCTION_OUTPUT_DIR:-$run_dir/production}
log_dir=${PIPELINE_LOG_DIR:-$run_dir/logs}
timings_path="$run_dir/stage-timings.jsonl"
resource_started="$run_dir/resource-escalation.started"
resource_complete="$run_dir/resource-escalation.complete"

if (( target_total != per_language * 5 )); then
    echo "TARGET_TOTAL must equal PER_LANGUAGE * 5" >&2
    exit 2
fi
if (( e2b_concurrency < 1 || e2b_concurrency > 20 )); then
    echo "E2B_CONCURRENCY must be between 1 and 20" >&2
    exit 2
fi
if (( verify_rounds < 1 )); then
    echo "VERIFY_ROUNDS must be at least 1" >&2
    exit 2
fi

mkdir -p "$crawl_dir" "$production_dir" "$log_dir"

run_stage() {
    local stage=$1
    shift
    local log_path="$log_dir/$stage.log"
    local started_at started_epoch finished_at finished_epoch status duration
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
    set -e

    finished_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    finished_epoch=$(date +%s)
    duration=$((finished_epoch - started_epoch))
    printf \
        '{"run_id":"%s","stage":"%s","started_at":"%s","finished_at":"%s","duration_s":%d,"exit_code":%d}\n' \
        "$run_id" "$stage" "$started_at" "$finished_at" "$duration" "$status" \
        >> "$timings_path"
    echo "[$finished_at] stage=$stage exit_code=$status duration_s=$duration" | tee -a "$log_path"
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
}

verify_until_drained() {
    local tier=$1
    local cpu_count=$2
    local memory_mb=$3
    local round before after delay
    for ((round = 1; round <= verify_rounds; round++)); do
        before=$(pending_count)
        if (( before == 0 )); then
            return 0
        fi
        run_stage "verify-$tier-round-$round" \
            env \
                PIPELINE_OUTPUT_DIR="$production_dir" \
                PIPELINE_E2B_CPU_COUNT="$cpu_count" \
                PIPELINE_E2B_MEMORY_MB="$memory_mb" \
                PIPELINE_E2B_CONCURRENCY="$e2b_concurrency" \
                PIPELINE_LANGUAGE_QUOTA_ENABLED=false \
                uv run alvance-github-crawler \
                --verify-pending \
                --e2b-concurrency "$e2b_concurrency" \
                --verbose
        after=$(pending_count)
        if (( after == 0 )); then
            return 0
        fi
        delay=$((round * 15))
        echo "pending=$after after tier=$tier round=$round; retrying in ${delay}s" \
            | tee -a "$log_dir/verify-$tier.log"
        sleep "$delay"
    done
    return 1
}

trap write_report EXIT

run_stage crawl \
    uv run alvance-github-crawler crawl \
    --target-total "$target_total" \
    --per-language "$per_language" \
    --output "$crawl_dir" \
    --verbose

run_stage prescreen \
    env \
        PIPELINE_OUTPUT_DIR="$production_dir" \
        PIPELINE_LANGUAGE_QUOTA_ENABLED=false \
        uv run alvance-github-crawler produce \
        --input "$crawl_dir/accepted_repositories.jsonl" \
        --defer-e2b \
        --verbose

if [[ -f "$resource_started" && ! -f "$resource_complete" ]]; then
    verify_until_drained escalated 2 4096 || {
        echo "resource-escalated verification remains incomplete; rerun with PIPELINE_RUN_ID=$run_id" >&2
        exit 3
    }
    touch "$resource_complete"
elif [[ ! -f "$resource_complete" ]]; then
    verify_until_drained default 1 1024 || {
        echo "default verification remains incomplete; rerun with PIPELINE_RUN_ID=$run_id" >&2
        exit 3
    }

    run_stage requeue-resource-failures \
        env PIPELINE_OUTPUT_DIR="$production_dir" \
        uv run alvance-github-crawler \
        --requeue-failures \
        --failure-reason e2b_resource_exhausted \
        --failure-reason benchmark_resource_fail \
        --failure-reason offline_test_timeout \
        --verbose
    touch "$resource_started"

    verify_until_drained escalated 2 4096 || {
        echo "resource-escalated verification remains incomplete; rerun with PIPELINE_RUN_ID=$run_id" >&2
        exit 3
    }
    touch "$resource_complete"
fi

write_report
trap - EXIT
echo "pipeline complete: $run_dir"
