#!/usr/bin/env bash
set -euo pipefail
base_commit=7480766908955b0ff5b232a7d2e60217732de5cb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
