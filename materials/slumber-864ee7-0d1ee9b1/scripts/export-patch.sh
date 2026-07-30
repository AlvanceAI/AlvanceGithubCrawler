#!/usr/bin/env bash
set -euo pipefail
base_commit=0d1ee9b1896d77274f06329a9ad79a3d7dab6b8d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
