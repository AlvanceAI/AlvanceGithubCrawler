#!/usr/bin/env bash
set -euo pipefail
base_commit=d6f6d12b38ad9d19e069a5d89d1973600cabcb73
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
