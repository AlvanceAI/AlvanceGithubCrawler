#!/usr/bin/env bash
set -euo pipefail
base_commit=5eab33ba5e8abc6e884daff66d3d91f1291351e3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
