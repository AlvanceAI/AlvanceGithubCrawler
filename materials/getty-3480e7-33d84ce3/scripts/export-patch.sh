#!/usr/bin/env bash
set -euo pipefail
base_commit=33d84ce338b4403e27073b79d9a54fcdc5c2337d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
