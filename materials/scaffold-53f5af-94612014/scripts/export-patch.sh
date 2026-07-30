#!/usr/bin/env bash
set -euo pipefail
base_commit=946120140678d1210e19dbbdecb1d973dae999eb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
