#!/usr/bin/env bash
set -euo pipefail
base_commit=66826172a3520a28ba414cae274d18f3d6ef0edd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
