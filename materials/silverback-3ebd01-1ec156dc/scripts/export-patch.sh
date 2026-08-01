#!/usr/bin/env bash
set -euo pipefail
base_commit=1ec156dc12cd142cb475a18280c1e8670058c339
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
