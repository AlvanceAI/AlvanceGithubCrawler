#!/usr/bin/env bash
set -euo pipefail
base_commit=c2f0ec3d6afb6f88ddfc93e5b4756e357db1807e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
