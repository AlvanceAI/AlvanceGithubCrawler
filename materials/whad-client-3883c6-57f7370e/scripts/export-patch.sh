#!/usr/bin/env bash
set -euo pipefail
base_commit=57f7370e58cc9d0d318f3986ac3808335251cea7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
