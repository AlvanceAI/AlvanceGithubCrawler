#!/usr/bin/env bash
set -euo pipefail
base_commit=b3cff101969b0c4455c546258cc4d1902a2f3543
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
