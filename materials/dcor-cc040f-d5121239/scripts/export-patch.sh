#!/usr/bin/env bash
set -euo pipefail
base_commit=d5121239dc50788f69ce95dd3c3cdbd2f5f4626c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
