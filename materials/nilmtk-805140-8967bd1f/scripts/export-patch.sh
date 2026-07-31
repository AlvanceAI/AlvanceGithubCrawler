#!/usr/bin/env bash
set -euo pipefail
base_commit=8967bd1fde24d0c8d89408179dd2499d8e60b4c3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
