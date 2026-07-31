#!/usr/bin/env bash
set -euo pipefail
base_commit=36ed5404a129598f5d3ddb528d932f44cad478f0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
