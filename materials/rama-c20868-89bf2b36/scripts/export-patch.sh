#!/usr/bin/env bash
set -euo pipefail
base_commit=89bf2b36c5700e9df33bf01df2e3a6a8f495cbf0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
