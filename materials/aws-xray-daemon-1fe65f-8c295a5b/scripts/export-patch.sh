#!/usr/bin/env bash
set -euo pipefail
base_commit=8c295a5b20dce58bb1ab38cd4a93e84b70449e94
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
