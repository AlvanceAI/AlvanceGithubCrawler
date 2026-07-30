#!/usr/bin/env bash
set -euo pipefail
base_commit=6f20abaa46a10f5317d13b4b5a3caf274ff13774
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
