#!/usr/bin/env bash
set -euo pipefail
base_commit=99bd6e013dc069320dc94833392efc0e9357d6e8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
