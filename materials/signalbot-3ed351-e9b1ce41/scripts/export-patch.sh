#!/usr/bin/env bash
set -euo pipefail
base_commit=e9b1ce411da05af1306d6827f5b5de20f0137809
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
