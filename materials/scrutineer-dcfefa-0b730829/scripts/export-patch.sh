#!/usr/bin/env bash
set -euo pipefail
base_commit=0b73082950a0d86308ff2a7acbdf7788aed5cc4c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
