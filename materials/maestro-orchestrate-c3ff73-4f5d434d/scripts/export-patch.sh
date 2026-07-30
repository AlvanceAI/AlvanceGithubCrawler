#!/usr/bin/env bash
set -euo pipefail
base_commit=4f5d434dded8a5e58808ad60f56c6e410f57cf7e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
