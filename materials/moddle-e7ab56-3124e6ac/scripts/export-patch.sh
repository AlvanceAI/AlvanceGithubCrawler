#!/usr/bin/env bash
set -euo pipefail
base_commit=3124e6ac3d5c06330e2e650973058c02b610df40
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
