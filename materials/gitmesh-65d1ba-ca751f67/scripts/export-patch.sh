#!/usr/bin/env bash
set -euo pipefail
base_commit=ca751f676ea5f60fcfc3c103fb7f24b8b455d0c0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
