#!/usr/bin/env bash
set -euo pipefail
base_commit=3f3cf9579987d520eef191d3f9b7d8c47d234276
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
