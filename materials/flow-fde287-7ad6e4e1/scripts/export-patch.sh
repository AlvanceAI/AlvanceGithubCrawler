#!/usr/bin/env bash
set -euo pipefail
base_commit=7ad6e4e19da5cd31a4a6fb241ce7f32ecb5f7b2a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
