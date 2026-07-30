#!/usr/bin/env bash
set -euo pipefail
base_commit=79e4899e43be5790b056eec3181c0d152ae8f496
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
