#!/usr/bin/env bash
set -euo pipefail
base_commit=a0f264ae8bd990e756f2e87c9b44610e522d801e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
