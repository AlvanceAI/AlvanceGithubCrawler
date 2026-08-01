#!/usr/bin/env bash
set -euo pipefail
base_commit=aa93d3f21c3bd983e8c55af88a175f06c3d32fc8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
