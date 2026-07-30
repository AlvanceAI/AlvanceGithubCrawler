#!/usr/bin/env bash
set -euo pipefail
base_commit=3d980f076fef130403e5fcccdac9510c234ca6fd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
