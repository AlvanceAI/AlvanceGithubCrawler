#!/usr/bin/env bash
set -euo pipefail
base_commit=07e0d3b97e963534bd0e129a9d758cb71f44ec92
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
