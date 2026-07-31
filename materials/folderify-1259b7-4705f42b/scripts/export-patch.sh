#!/usr/bin/env bash
set -euo pipefail
base_commit=4705f42b946ac7950c0431f0b0f39e9d6811a3fe
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
