#!/usr/bin/env bash
set -euo pipefail
base_commit=c69a7dbd0c3d7c10d350bff30b12b705217aa184
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
