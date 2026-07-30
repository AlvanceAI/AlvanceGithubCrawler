#!/usr/bin/env bash
set -euo pipefail
base_commit=b8c17d34316352c6eef864b6c49b23a4bcb10421
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
