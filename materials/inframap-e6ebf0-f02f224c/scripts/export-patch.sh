#!/usr/bin/env bash
set -euo pipefail
base_commit=f02f224cb0d0d8f369f001405fa646c206614b21
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
