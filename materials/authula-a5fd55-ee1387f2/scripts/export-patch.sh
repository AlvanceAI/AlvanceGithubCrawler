#!/usr/bin/env bash
set -euo pipefail
base_commit=ee1387f25b02f5951c61d66196c046e38f639bed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
