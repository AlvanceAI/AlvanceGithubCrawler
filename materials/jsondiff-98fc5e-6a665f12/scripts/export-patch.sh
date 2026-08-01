#!/usr/bin/env bash
set -euo pipefail
base_commit=6a665f12e1c4bc4c8291b58dc3f27ac03841133f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
