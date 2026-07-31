#!/usr/bin/env bash
set -euo pipefail
base_commit=6f5cec8c7937a0c1aeb3c35763a7042c4f6af13a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
