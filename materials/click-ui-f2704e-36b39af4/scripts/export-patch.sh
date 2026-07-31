#!/usr/bin/env bash
set -euo pipefail
base_commit=36b39af4b4efd9f18cfb866c580f1527ac16b3a5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
