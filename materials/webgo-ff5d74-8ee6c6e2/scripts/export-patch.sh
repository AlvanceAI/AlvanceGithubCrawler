#!/usr/bin/env bash
set -euo pipefail
base_commit=8ee6c6e23f3b325ba8495d6356096606dfedf510
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
