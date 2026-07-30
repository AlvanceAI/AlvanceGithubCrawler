#!/usr/bin/env bash
set -euo pipefail
base_commit=cfc8221b4b539930cc03a38f7e5fa17b3d3c3f56
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
