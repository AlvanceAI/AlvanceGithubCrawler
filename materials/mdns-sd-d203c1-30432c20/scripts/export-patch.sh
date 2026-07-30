#!/usr/bin/env bash
set -euo pipefail
base_commit=30432c20738f8efbf373c7333075e4e4532228ff
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
