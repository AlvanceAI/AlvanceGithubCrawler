#!/usr/bin/env bash
set -euo pipefail
base_commit=3f1ea98b8cca557cc8aa522e30f3c6976a044346
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
