#!/usr/bin/env bash
set -euo pipefail
base_commit=9895e3dea3ec44fbd452f57e2ff74d20acce9b5c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
