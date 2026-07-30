#!/usr/bin/env bash
set -euo pipefail
base_commit=6fb919871e244ea2a06b0a1af281d695d19862cf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
