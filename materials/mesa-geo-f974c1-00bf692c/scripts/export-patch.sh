#!/usr/bin/env bash
set -euo pipefail
base_commit=00bf692c0d4bf20c0a67c82df2b56a7230c81de7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
