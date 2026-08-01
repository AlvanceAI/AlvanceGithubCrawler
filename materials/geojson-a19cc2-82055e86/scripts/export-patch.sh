#!/usr/bin/env bash
set -euo pipefail
base_commit=82055e8679bbcdef5bd7fc0a3c7168e86cbd3d12
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
