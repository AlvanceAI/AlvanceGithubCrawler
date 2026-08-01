#!/usr/bin/env bash
set -euo pipefail
base_commit=d93116f2347cefa4b1d7f61ee35d629f786f6354
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
