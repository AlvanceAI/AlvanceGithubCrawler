#!/usr/bin/env bash
set -euo pipefail
base_commit=e25fd81bd08d2c99b8d39c16ada5a8246bbe80c6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
