#!/usr/bin/env bash
set -euo pipefail
base_commit=f8b184bca577f5fccce3f0e8eaf01cd8c537ee65
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
