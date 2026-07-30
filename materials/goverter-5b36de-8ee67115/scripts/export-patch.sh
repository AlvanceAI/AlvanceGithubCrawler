#!/usr/bin/env bash
set -euo pipefail
base_commit=8ee671150d0f50c81102177c6dafcb1482802adf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
