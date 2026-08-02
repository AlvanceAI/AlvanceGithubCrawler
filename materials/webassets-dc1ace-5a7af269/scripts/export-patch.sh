#!/usr/bin/env bash
set -euo pipefail
base_commit=5a7af269789a6e0da1f22dc114b02c117d79e8fe
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
