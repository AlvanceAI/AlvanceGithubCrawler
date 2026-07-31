#!/usr/bin/env bash
set -euo pipefail
base_commit=6609ced648afa6acc4a87389ea3a468139d1cd8e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
