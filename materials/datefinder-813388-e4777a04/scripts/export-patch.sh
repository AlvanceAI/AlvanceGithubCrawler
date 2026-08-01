#!/usr/bin/env bash
set -euo pipefail
base_commit=e4777a04fce8677aa816f6fc016f2848fe8ccaf5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
