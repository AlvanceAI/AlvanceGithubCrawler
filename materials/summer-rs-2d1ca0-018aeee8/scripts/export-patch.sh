#!/usr/bin/env bash
set -euo pipefail
base_commit=018aeee8c9b483a0f4851f14e9761c876cb544cc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
