#!/usr/bin/env bash
set -euo pipefail
base_commit=3ec062c3b6dc4d7d645974f3d79707f29bb9a0e9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
