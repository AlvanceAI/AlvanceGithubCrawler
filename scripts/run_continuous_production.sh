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
pending_low_watermark=${PENDING_LOW_WATERMARK:-120}
pending_high_watermark=${PENDING_HIGH_WATERMARK:-480}
crawl_validation_retries=${CRAWL_VALIDATION_RETRIES:-2}
crawl_retry_delay=${CRAWL_RETRY_DELAY_S:-5}
run_id=${PIPELINE_RUN_ID:-github-mass-production-$(date -u +%Y%m%dT%H%M%SZ)}
run_root=${PIPELINE_RUN_ROOT:-outputs/production-runs}
run_dir="$run_root/$run_id"
crawl_dir=${CRAWL_OUTPUT_DIR:-outputs/github_crawl_500_unquota}
production_dir=${PRODUCTION_OUTPUT_DIR:-outputs/github_production_500_unquota}
log_dir="$run_dir/logs"
timings_path="$run_dir/stage-timings.jsonl"
crawl_done="$run_dir/crawl.done"
crawl_status="$run_dir/crawl.status"
crawl_exhausted="$run_dir/crawl-exhausted"
prescreen_done="$run_dir/prescreen.done"
prescreen_status="$run_dir/prescreen.status"
e2b_done="$run_dir/e2b.done"
e2b_status="$run_dir/e2b.status"
e2b_follow_status="$run_dir/e2b-follow.status.json"
prescreen_follow_status="$run_dir/prescreen-follow.status.json"
producer_pid=""
crawl_pid=""
prescreen_pid=""
e2b_pid=""
background_pid=""
keys_exhausted="$run_dir/e2b-keys-exhausted"
cycle_complete="$run_dir/production-cycle-complete"
report_doc="docs/continuous-production-$run_id.md"
publish_tasks=${PUBLISH_TASKS:-true}
publish_run_artifacts=${PUBLISH_RUN_ARTIFACTS:-true}
auto_git_push=${AUTO_GIT_PUSH:-false}
user_cache_root=${XDG_CACHE_HOME:-${HOME}/.cache}
workspace_tmp_base=${PIPELINE_WORKSPACE_TMPDIR:-$user_cache_root/alvance-github-crawler/workspaces}
workspace_min_free_mb=${PIPELINE_WORKSPACE_MIN_FREE_MB:-20480}
workspace_max_mb=${PIPELINE_WORKSPACE_MAX_MB:-51200}
workspace_reservation_mb=${PIPELINE_WORKSPACE_RESERVATION_MB:-640}
workspace_quota_wait_s=${PIPELINE_WORKSPACE_QUOTA_WAIT_S:-900}
workspace_tmp_dir=""
producer_exit=0
crawl_exit=0
prescreen_exit=0
e2b_exit=0

for command_name in df du flock git gzip jq mktemp uv; do
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
if (( pending_low_watermark < 0 || pending_high_watermark <= pending_low_watermark )); then
    echo "pending watermarks must satisfy 0 <= low < high" >&2
    exit 2
fi
if (( crawl_validation_retries < 0 || crawl_validation_retries > 5 )); then
    echo "CRAWL_VALIDATION_RETRIES must be between 0 and 5" >&2
    exit 2
fi
if (( crawl_retry_delay < 0 || crawl_retry_delay > 300 )); then
    echo "CRAWL_RETRY_DELAY_S must be between 0 and 300" >&2
    exit 2
fi
if [[ $auto_git_push != false ]]; then
    echo "automatic git push is disabled by this production entrypoint; unset AUTO_GIT_PUSH" >&2
    exit 2
fi
if [[ ! $workspace_min_free_mb =~ ^[0-9]+$ ]] || (( workspace_min_free_mb < 1024 )); then
    echo "PIPELINE_WORKSPACE_MIN_FREE_MB must be an integer of at least 1024" >&2
    exit 2
fi
if [[ ! $workspace_max_mb =~ ^[0-9]+$ ]] || (( workspace_max_mb < 1024 )); then
    echo "PIPELINE_WORKSPACE_MAX_MB must be an integer of at least 1024" >&2
    exit 2
fi
if [[ ! $workspace_reservation_mb =~ ^[0-9]+$ ]] \
    || (( workspace_reservation_mb < 64 || workspace_reservation_mb > workspace_max_mb )); then
    echo "PIPELINE_WORKSPACE_RESERVATION_MB must be between 64 and PIPELINE_WORKSPACE_MAX_MB" >&2
    exit 2
fi
if [[ ! $workspace_quota_wait_s =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    echo "PIPELINE_WORKSPACE_QUOTA_WAIT_S must be a non-negative number" >&2
    exit 2
fi
if [[ $(git branch --show-current) != "$publish_branch" ]]; then
    echo "continuous production must run on branch $publish_branch" >&2
    exit 2
fi

mkdir -p "$crawl_dir" "$production_dir" "$log_dir"
rm -f \
    "$crawl_done" "$crawl_status" \
    "$crawl_exhausted" \
    "$prescreen_done" "$prescreen_status" \
    "$e2b_done" "$e2b_status" "$e2b_follow_status" \
    "$prescreen_follow_status" "$keys_exhausted" "$cycle_complete"

restore_raw_crawl_snapshot() {
    local raw_path="$crawl_dir/raw_repositories.jsonl"
    local archive_path="$raw_path.gz"
    if [[ ! -s $raw_path && -s $archive_path ]]; then
        echo "restoring local raw crawl checkpoint from $archive_path"
        gzip -dc -- "$archive_path" > "$raw_path"
    fi
}

initialize_workspace() {
    local lock_path="$repo_root/.crawler-state/continuous-production.lock"
    local stale_dir
    mkdir -p "$repo_root/.crawler-state" "$workspace_tmp_base"
    workspace_tmp_base=$(cd "$workspace_tmp_base" && pwd -P)

    exec 9>"$lock_path"
    if ! flock -n 9; then
        echo "another continuous production driver already owns $lock_path" >&2
        return 3
    fi

    while IFS= read -r -d '' stale_dir; do
        [[ -f $stale_dir/.alvance-production-workspace ]] || continue
        find "$stale_dir" -mindepth 1 -depth -delete 2>/dev/null || true
        rmdir "$stale_dir" 2>/dev/null || true
    done < <(find "$workspace_tmp_base" -mindepth 1 -maxdepth 1 -type d -print0)

    workspace_tmp_dir=$(mktemp -d "$workspace_tmp_base/${run_id}.XXXXXX")
    touch "$workspace_tmp_dir/.alvance-production-workspace"
    export TMPDIR="$workspace_tmp_dir"
    export ALVANCE_WORKSPACE_TMPDIR="$workspace_tmp_dir"
    export ALVANCE_WORKSPACE_MAX_MB="$workspace_max_mb"
    export ALVANCE_WORKSPACE_RESERVATION_MB="$workspace_reservation_mb"
    export ALVANCE_WORKSPACE_QUOTA_WAIT_S="$workspace_quota_wait_s"
}

workspace_free_mb() {
    df -Pm "$workspace_tmp_dir" | awk 'NR == 2 { print $4 }'
}

workspace_used_mb() {
    du -sm "$workspace_tmp_dir" | awk 'NR == 1 { print $1 }'
}

ensure_workspace_capacity() {
    local free_mb used_mb
    free_mb=$(workspace_free_mb)
    used_mb=$(workspace_used_mb)
    if [[ ! $free_mb =~ ^[0-9]+$ ]]; then
        echo "unable to determine free space for workspace $workspace_tmp_dir" >&2
        return 75
    fi
    if (( free_mb < workspace_min_free_mb )); then
        echo "workspace free space is ${free_mb}MB; at least ${workspace_min_free_mb}MB is required" >&2
        return 75
    fi
    if [[ ! $used_mb =~ ^[0-9]+$ ]] || (( used_mb >= workspace_max_mb )); then
        echo "workspace usage is ${used_mb:-unknown}MB; quota is ${workspace_max_mb}MB" >&2
        return 75
    fi
}

cleanup_workspace() {
    if [[ -z $workspace_tmp_dir || ! -d $workspace_tmp_dir ]]; then
        return 0
    fi
    find "$workspace_tmp_dir" -mindepth 1 -depth -delete 2>/dev/null || true
    rmdir "$workspace_tmp_dir" 2>/dev/null || true
    workspace_tmp_dir=""
}

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
    if git diff --cached --quiet -- catalog materials tasks; then
        return 0
    fi
    git commit -m "chore(tasks): publish $run_id batch $(date -u +%Y%m%dT%H%M%SZ)" \
        -- catalog materials tasks
    push_if_enabled
}

push_if_enabled() {
    echo "automatic git push disabled; push manually with: git push origin $publish_branch"
}

publish_final_report() {
    [[ $publish_run_artifacts == true ]] || return 0
    local raw_path="$crawl_dir/raw_repositories.jsonl"
    local raw_archive="$raw_path.gz"
    local raw_was_tracked=false
    if [[ -s $raw_path ]]; then
        gzip -9c -- "$raw_path" > "$raw_archive"
    fi
    # Keep raw API payloads local, while retaining a compact resume snapshot in Git.
    if git ls-files --error-unmatch -- "$raw_path" >/dev/null 2>&1; then
        raw_was_tracked=true
        git rm --cached -- "$raw_path"
    fi
    git add -- \
        "$raw_archive" \
        "$crawl_dir/accepted_repositories.jsonl" \
        "$crawl_dir/crawl_state.json" \
        "$crawl_dir/rejected_repositories.jsonl" \
        "$crawl_dir/summary.json" \
        "$production_dir" \
        "$run_dir" \
        "$report_doc"
    local report_paths=(
        "$raw_archive"
        "$crawl_dir/accepted_repositories.jsonl"
        "$crawl_dir/crawl_state.json"
        "$crawl_dir/rejected_repositories.jsonl"
        "$crawl_dir/summary.json"
        "$production_dir"
        "$run_dir"
        "$report_doc"
    )
    if [[ $raw_was_tracked == true ]]; then
        report_paths+=("$raw_path")
    fi
    if git diff --cached --quiet -- "${report_paths[@]}"; then
        return 0
    fi
    git commit -m "docs: record $run_id production statistics" -- "${report_paths[@]}"
    push_if_enabled
}

current_per_language() {
    if [[ -s "$crawl_dir/crawl_state.json" ]]; then
        jq -r '.per_language // 0' "$crawl_dir/crawl_state.json"
        return
    fi
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

crawl_checkpoint_complete() {
    local target=$1
    [[ -s $crawl_dir/summary.json ]] || return 1
    jq -e --argjson target "$target" '
        .status == "completed"
        and ((.validation_errors // []) | length == 0)
        and (
            (.target_total == $target
                and .fetched_total == $target
                and .deduplicated_total == $target)
            or (.exhausted_without_full_target == true
                and (.fetched_total // 0) == (.deduplicated_total // -1))
        )
    ' "$crawl_dir/summary.json" >/dev/null
}

crawl_checkpoint_exhausted() {
    [[ -s "$crawl_dir/crawl_state.json" ]] || return 1
    jq -e '
        .completed == true
        and ((.exhausted_languages // []) | length == 5)
    ' "$crawl_dir/crawl_state.json" >/dev/null
}

recoverable_crawl_validation_failure() {
    local target=$1
    [[ -s $crawl_dir/summary.json ]] || return 1
    jq -e --argjson target "$target" '
        .status == "incomplete"
        and .target_total == $target
        and ((.validation_errors // []) | length > 0)
        and all(
            (.validation_errors // [])[];
            test(
                "^(raw count is |unique raw count is |raw (python|go|typescript|javascript|rust) count is |accepted and rejected records do not cover)"
            )
        )
    ' "$crawl_dir/summary.json" >/dev/null
}

run_crawl_batch() {
    local target=$1
    local per_language=$2
    local attempt=0 stage status
    while true; do
        stage="crawl-$target"
        if (( attempt > 0 )); then
            stage="crawl-$target-retry-$attempt"
        fi
        if run_stage "$stage" \
            uv run alvance-github-crawler crawl \
            --target-total "$target" \
            --per-language "$per_language" \
            --max-search-pages 10 \
            --output "$crawl_dir" \
            --request-interval 0.2 \
            --verbose; then
            if jq -e '.exhausted_without_full_target == true' "$crawl_dir/summary.json" >/dev/null 2>&1; then
                touch "$crawl_exhausted"
                echo "crawl completed with all language searches exhausted" \
                    | tee -a "$log_dir/crawl-recovery.log"
            fi
            return 0
        else
            status=$?
        fi

        # Search exhaustion is a normal terminal state when every language has
        # no further results. The crawler still leaves a resumable checkpoint;
        # the prescreen follower must consume its final accepted records.
        if crawl_checkpoint_exhausted \
            && grep -q "all GitHub language searches are exhausted" "$log_dir/$stage.log"; then
            touch "$crawl_exhausted"
            echo "crawl search exhausted; continuing with available raw sample" \
                | tee -a "$log_dir/crawl-recovery.log"
            return 0
        fi

        if (( attempt >= crawl_validation_retries )) \
            || ! recoverable_crawl_validation_failure "$target"; then
            return "$status"
        fi
        attempt=$((attempt + 1))
        echo "recoverable crawl checkpoint mismatch at target=$target; retry $attempt/$crawl_validation_retries after ${crawl_retry_delay}s" \
            | tee -a "$log_dir/crawl-recovery.log"
        sleep "$crawl_retry_delay"
    done
}

run_prescreen() {
    local stage=$1
    ensure_workspace_capacity || return $?
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

produce_crawl_candidates() {
    local checkpoint_per checkpoint_target target_per target
    checkpoint_per=0
    checkpoint_target=0
    if [[ -s "$crawl_dir/crawl_state.json" ]]; then
        checkpoint_per=$(jq -r '.per_language // 0' "$crawl_dir/crawl_state.json")
        checkpoint_target=$(jq -r '.target_total // 0' "$crawl_dir/crawl_state.json")
    fi
    [[ $checkpoint_per =~ ^[0-9]+$ ]] || checkpoint_per=0
    [[ $checkpoint_target =~ ^[0-9]+$ ]] || checkpoint_target=0

    # A resumed checkpoint is never reduced. This matters when one language has
    # been exhausted and its quota was redistributed to the remaining searches.
    target_per=$max_per_language
    if (( checkpoint_per > target_per )); then
        target_per=$checkpoint_per
    fi
    target=$((target_per * 5))
    if (( checkpoint_target > target )); then
        target=$checkpoint_target
    fi
    if crawl_checkpoint_complete "$target"; then
        echo "crawl checkpoint already complete: target=$target"
        if jq -e '.exhausted_without_full_target == true' "$crawl_dir/summary.json" >/dev/null 2>&1; then
            touch "$crawl_exhausted"
        fi
        return 0
    fi
    if crawl_checkpoint_exhausted; then
        touch "$crawl_exhausted"
        echo "crawl checkpoint has exhausted all language searches; resuming screening"
        return 0
    fi

    # CandidateCrawler itself appends each 100-result GitHub page and every
    # accepted record immediately. One long-lived crawl avoids repeatedly
    # reparsing the growing raw snapshot between artificial shell batches.
    run_crawl_batch "$target" "$target_per"
}

start_background_stage() {
    local stage=$1 status_path=$2 done_path=$3
    shift 3
    (
        set +e
        run_stage "$stage" "$@"
        local status=$?
        printf '%d\n' "$status" > "$status_path"
        touch "$done_path"
        exit "$status"
    ) &
    background_pid=$!
}

start_crawl_producer() {
    start_background_stage crawl-producer "$crawl_status" "$crawl_done" produce_crawl_candidates
    crawl_pid=$background_pid
    producer_pid=$background_pid
}

start_prescreen_follower() {
    ensure_workspace_capacity || return $?
    start_background_stage prescreen-follow "$prescreen_status" "$prescreen_done" \
        env \
            PIPELINE_OUTPUT_DIR="$production_dir" \
            PIPELINE_LANGUAGE_QUOTA_ENABLED=false \
            PIPELINE_PRESCREEN_CONCURRENCY="$prescreen_concurrency" \
            uv run alvance-github-crawler produce \
            --input "$crawl_dir/accepted_repositories.jsonl" \
            --input-cursor "$crawl_dir/accepted_repositories.cursor.json" \
            --input-done "$crawl_done" \
            --follow-input \
            --follow-status "$prescreen_follow_status" \
            --follow-poll-interval 2 \
            --pending-high-watermark "$pending_high_watermark" \
            --pending-low-watermark "$pending_low_watermark" \
            --prescreen-concurrency "$prescreen_concurrency" \
            --defer-e2b \
            --verbose
    prescreen_pid=$background_pid
}

start_e2b_follower() {
    ensure_workspace_capacity || return $?
    start_background_stage verify-follow-default "$e2b_status" "$e2b_done" \
        env \
            PIPELINE_OUTPUT_DIR="$production_dir" \
            PIPELINE_E2B_CPU_COUNT=1 \
            PIPELINE_E2B_MEMORY_MB=1024 \
            PIPELINE_E2B_CONCURRENCY="$per_key_concurrency" \
            PIPELINE_LANGUAGE_QUOTA_ENABLED=false \
            uv run alvance-github-crawler \
            --verify-pending \
            --follow-until "$prescreen_done" \
            --follow-status "$e2b_follow_status" \
            --follow-poll-interval 2 \
            --e2b-concurrency "$per_key_concurrency" \
            --verbose
    e2b_pid=$background_pid
}

stop_background_stage() {
    local pid=$1
    if [[ -n $pid ]] && kill -0 "$pid" 2>/dev/null; then
        kill -TERM "$pid" 2>/dev/null || true
        wait "$pid" 2>/dev/null || true
    fi
}

stop_producer() {
    stop_background_stage "$e2b_pid"
    stop_background_stage "$prescreen_pid"
    stop_background_stage "$crawl_pid"
    e2b_pid=""
    prescreen_pid=""
    crawl_pid=""
    producer_pid=""
}

verify_once() {
    local tier=$1
    local cpu_count=$2
    local memory_mb=$3
    local status
    ensure_workspace_capacity || return $?
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
            if [[ $wait_for_producer == true && ! -f $prescreen_done ]]; then
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
        if (( status == 75 )); then
            return 75
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
    cleanup_workspace
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

initialize_workspace
ensure_workspace_capacity
restore_raw_crawl_snapshot

doctor_json=$(
    PIPELINE_E2B_CONCURRENCY="$per_key_concurrency" \
    PIPELINE_PRESCREEN_CONCURRENCY="$prescreen_concurrency" \
        uv run alvance-github-crawler --doctor
)
github_ready=$(jq -r '.github_token // false' <<< "$doctor_json")
github_token_count=$(jq -r '.github_token_count // 0' <<< "$doctor_json")
openai_ready=$(jq -r '.openai_api_key // false' <<< "$doctor_json")
openai_sdk_ready=$(jq -r '.openai_sdk // false' <<< "$doctor_json")
e2b_sdk_ready=$(jq -r '.e2b_sdk // false' <<< "$doctor_json")
key_count=$(jq -r '.e2b_api_key_count // 0' <<< "$doctor_json")
total_concurrency=$(jq -r '.e2b_total_concurrency // 0' <<< "$doctor_json")

if [[ $github_ready != true ]]; then
    echo "missing GitHub credentials; set GITHUB_TOKEN1/GITHUB_TOKEN2 (or GITHUB_TOKEN) in .env or authenticate gh" >&2
    exit 2
fi
if (( github_token_count < 1 )); then
    echo "doctor found no usable GitHub token; set GITHUB_TOKEN1/GITHUB_TOKEN2 in .env" >&2
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
if (( key_count < 1 || total_concurrency != per_key_concurrency * key_count )); then
    echo "expected E2B_API_KEY or at least one numbered E2B API key in .env; configured slots=$((per_key_concurrency * key_count))" >&2
    exit 2
fi
echo "preflight passed: branch=$publish_branch github_tokens=$github_token_count prescreen=$prescreen_concurrency e2b_keys=$key_count e2b_slots=$total_concurrency workspace=$workspace_tmp_dir workspace_free_mb=$(workspace_free_mb) workspace_quota_mb=$workspace_max_mb workspace_reservation_mb=$workspace_reservation_mb workspace_slots=$((workspace_max_mb / workspace_reservation_mb))"

if [[ -s catalog/e2b-packages.jsonl ]]; then
    ensure_workspace_capacity
    run_stage repair-rebuildable-packages \
        uv run python scripts/repair_rebuildable_tasks.py \
        --root "$repo_root" \
        --workers "$package_repair_workers"
fi

# Reopen failures caused by recipes or transient capacity handling fixed in this
# release. Markers make this safe to execute on every resumed production run.
run_stage requeue-node-package-manager-v18 \
    env PIPELINE_OUTPUT_DIR="$production_dir" \
    uv run alvance-github-crawler \
    --requeue-failures \
    --failure-reason build_fail \
    --failure-contains "can only install with an existing package-lock.json" \
    --requeue-marker node-package-manager-v18 \
    --verbose

run_stage requeue-go-runtime-v4 \
    env PIPELINE_OUTPUT_DIR="$production_dir" \
    uv run alvance-github-crawler \
    --requeue-failures \
    --failure-reason infra_error \
    --failure-contains "toolchain not available" \
    --requeue-marker go-runtime-v4 \
    --verbose

run_stage requeue-e2b-rate-limit-backoff-v1 \
    env PIPELINE_OUTPUT_DIR="$production_dir" \
    uv run alvance-github-crawler \
    --requeue-failures \
    --failure-reason infra_error \
    --failure-reason stage_error \
    --failure-contains "maximum number of concurrent" \
    --requeue-marker e2b-rate-limit-backoff-v1 \
    --verbose

retry_disk_space_failures() {
    local marker="$run_dir/disk-space-retry-v1.done"
    local rejection_path="$production_dir/rejections.jsonl"
    local -a repositories command
    [[ -f $marker ]] && return 0
    if [[ ! -s $rejection_path || ! -s $crawl_dir/accepted_repositories.jsonl ]]; then
        touch "$marker"
        return 0
    fi

    mapfile -t repositories < <(
        jq -r -s '
            reduce .[] as $event ({}; .[$event.repo // ""] = $event)
            | .[]
            | select(.repo and .stage == "stage2_checkout" and .reason == "stage_error")
            | select(
                (.error // "")
                | test(
                    "No space left on device|failed to write new configuration file|unable to write file|write returned";
                    "i"
                )
            )
            | .repo
        ' "$rejection_path"
    )
    if (( ${#repositories[@]} == 0 )); then
        touch "$marker"
        return 0
    fi

    ensure_workspace_capacity || return $?
    command=(
        env
        "PIPELINE_OUTPUT_DIR=$production_dir"
        PIPELINE_LANGUAGE_QUOTA_ENABLED=false
        "PIPELINE_PRESCREEN_CONCURRENCY=$prescreen_concurrency"
        uv run alvance-github-crawler produce
        --input "$crawl_dir/accepted_repositories.jsonl"
        --prescreen-concurrency "$prescreen_concurrency"
        --retry-rejected
        --defer-e2b
        --verbose
    )
    for repository in "${repositories[@]}"; do
        command+=(--repository "$repository")
    done
    run_stage retry-disk-space-v1 "${command[@]}" || return $?
    touch "$marker"
}

retry_disk_space_failures

start_crawl_producer
start_prescreen_follower
start_e2b_follower

# E2B remains alive while the other two stages are producing. It is the first
# stage to finish in the normal case, because its follow marker is written only
# after prescreen has finished and pending has drained.
set +e
wait "$e2b_pid"
e2b_exit=$?
set -e
e2b_pid=""

consumer_status=0
if (( e2b_exit == 4 )); then
    touch "$keys_exhausted"
    echo "E2B key pool exhausted; stopping upstream followers" >&2
    stop_producer
elif (( e2b_exit != 0 )); then
    echo "E2B follower stopped with exit code $e2b_exit; stopping upstream followers" >&2
    stop_producer
else
    set +e
    wait "$prescreen_pid"
    prescreen_exit=$?
    wait "$crawl_pid"
    crawl_exit=$?
    set -e
    prescreen_pid=""
    crawl_pid=""
    if [[ -s "$prescreen_status" ]]; then
        prescreen_exit=$(cat "$prescreen_status")
    fi
    if [[ -s "$crawl_status" ]]; then
        crawl_exit=$(cat "$crawl_status")
    fi

    if (( crawl_exit != 0 || prescreen_exit != 0 )); then
        echo "upstream follower failed: crawl=$crawl_exit prescreen=$prescreen_exit" >&2
    else
        run_stage requeue-resource-failures \
            env PIPELINE_OUTPUT_DIR="$production_dir" \
            uv run alvance-github-crawler \
            --requeue-failures \
            --failure-reason e2b_resource_exhausted \
            --failure-reason benchmark_resource_fail \
            --failure-reason offline_test_timeout \
            --requeue-marker resource-escalation-c2-m4096-v1 \
            --verbose

        set +e
        consume_until_idle escalated 2 4096 false
        consumer_status=$?
        set -e
    fi
fi

write_report
publish_completed_tasks

if [[ -f $keys_exhausted || $e2b_exit == 4 || $consumer_status == 4 ]]; then
    publish_final_report
    cleanup_workspace
    trap - EXIT INT TERM
    echo "continuous production stopped: all configured E2B key slots exhausted"
    exit 4
fi
if (( crawl_exit != 0 )); then
    cleanup_workspace
    trap - EXIT INT TERM
    echo "continuous production failed: crawl exit=$crawl_exit; report remains local" >&2
    exit "$crawl_exit"
fi
if (( prescreen_exit != 0 )); then
    cleanup_workspace
    trap - EXIT INT TERM
    echo "continuous production failed: prescreen exit=$prescreen_exit; report remains local" >&2
    exit "$prescreen_exit"
fi
if (( e2b_exit != 0 )); then
    cleanup_workspace
    trap - EXIT INT TERM
    echo "continuous production failed: E2B follower exit=$e2b_exit; report remains local" >&2
    exit "$e2b_exit"
fi
if (( consumer_status != 0 )); then
    cleanup_workspace
    trap - EXIT INT TERM
    echo "continuous production failed: consumer exit=$consumer_status; report remains local" >&2
    exit "$consumer_status"
fi

publish_final_report
touch "$cycle_complete"
cleanup_workspace
trap - EXIT INT TERM
echo "continuous production complete: $run_dir"
