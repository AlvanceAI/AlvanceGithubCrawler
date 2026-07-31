#!/usr/bin/env bash
set -euo pipefail
base_commit=3b45f0887a8c8dc1d4c59fc7c0f5700b38df44e0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
