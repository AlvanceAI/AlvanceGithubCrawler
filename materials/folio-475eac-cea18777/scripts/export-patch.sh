#!/usr/bin/env bash
set -euo pipefail
base_commit=cea18777bc558fe446b9b03c7d4dc62368e9d231
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
