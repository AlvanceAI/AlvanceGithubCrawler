#!/usr/bin/env bash
set -euo pipefail
base_commit=2dc17e7722e73e6b6868c2ec0ced062bb32e4cc1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
