#!/usr/bin/env bash
set -euo pipefail
base_commit=95bf09333831cdcff2c0852051a25a3fae630e94
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
