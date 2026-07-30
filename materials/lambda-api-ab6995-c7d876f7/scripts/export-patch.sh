#!/usr/bin/env bash
set -euo pipefail
base_commit=c7d876f734c5cad5248d954f997353ca9af72292
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
