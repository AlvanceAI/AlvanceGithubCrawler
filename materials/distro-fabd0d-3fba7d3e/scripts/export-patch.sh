#!/usr/bin/env bash
set -euo pipefail
base_commit=3fba7d3e19c84e5bb1f15c22b1a5a6db6e8f07c7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
