#!/usr/bin/env bash
set -euo pipefail
base_commit=26729f5260e010440f00b4e3130efde96661ce2d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
