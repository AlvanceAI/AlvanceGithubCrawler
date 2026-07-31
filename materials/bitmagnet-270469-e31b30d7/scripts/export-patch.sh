#!/usr/bin/env bash
set -euo pipefail
base_commit=e31b30d7351c269dc801876f92ebc59d31fee545
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
