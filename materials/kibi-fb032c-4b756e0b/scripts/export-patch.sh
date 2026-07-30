#!/usr/bin/env bash
set -euo pipefail
base_commit=4b756e0be889037c34e5d6179f440dd8cd414345
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
