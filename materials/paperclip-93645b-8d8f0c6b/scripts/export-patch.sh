#!/usr/bin/env bash
set -euo pipefail
base_commit=8d8f0c6b0772308962c6f1617305f073fbed630c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
