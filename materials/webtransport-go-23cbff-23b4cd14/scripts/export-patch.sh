#!/usr/bin/env bash
set -euo pipefail
base_commit=23b4cd1439e9ed2d9c9d412f9d869a0e24c5eabf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
