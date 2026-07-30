#!/usr/bin/env bash
set -euo pipefail
base_commit=f554eeb69e9ef510ee58dfd6e1cbcf2d13ae06c5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
