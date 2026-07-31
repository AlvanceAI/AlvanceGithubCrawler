#!/usr/bin/env bash
set -euo pipefail
base_commit=9e827d8ecf9072101ca6fc84f20f2c30c8ef0f74
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
