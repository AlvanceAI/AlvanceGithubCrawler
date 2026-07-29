#!/usr/bin/env bash
set -euo pipefail
base_commit=316a0f15fbbd6923213cc1f7df3f7e8ea28e1975
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
