#!/usr/bin/env bash
set -euo pipefail
base_commit=bdf3096a6413e4e5ba90ea5890224f847f676faa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
