#!/usr/bin/env bash
set -euo pipefail
base_commit=e56c6d5f837b350089305690c80377ceba024989
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
