#!/usr/bin/env bash
set -euo pipefail
base_commit=f92eff61fa1594e8008e198fbfc2ac537cd776e6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
