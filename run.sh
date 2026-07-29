#!/bin/bash
# Continuous pipeline: discover → verify → repeat
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="/tmp/alvance-crawler.log"
BATCH_DISCOVER="${BATCH_DISCOVER:-100}"
BATCH_VERIFY="${BATCH_VERIFY:-20}"
SLEEP_BETWEEN="${SLEEP_BETWEEN:-10}"

cd "$REPO_DIR"

echo "[$(date)] Starting continuous pipeline (discover=$BATCH_DISCOVER verify=$BATCH_VERIFY)" | tee -a "$LOG"

while true; do
    echo "[$(date)] === Discover phase ===" | tee -a "$LOG"
    alvance-github-crawler --defer-e2b --max-repos "$BATCH_DISCOVER" --verbose 2>&1 | tee -a "$LOG"

    echo "[$(date)] === Verify phase ===" | tee -a "$LOG"
    alvance-github-crawler --verify-pending --max-repos "$BATCH_VERIFY" --verbose 2>&1 | tee -a "$LOG"

    echo "[$(date)] Sleeping ${SLEEP_BETWEEN}s..." | tee -a "$LOG"
    sleep "$SLEEP_BETWEEN"
done
