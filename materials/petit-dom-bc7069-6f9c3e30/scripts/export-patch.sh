#!/usr/bin/env bash
set -euo pipefail
base_commit=6f9c3e30f4a515a470f50df3d3d85944bca66d71
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
