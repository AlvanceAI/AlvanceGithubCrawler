#!/usr/bin/env bash
set -euo pipefail
base_commit=6246d09bc943070619d9114f85af70fc1acc719a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
