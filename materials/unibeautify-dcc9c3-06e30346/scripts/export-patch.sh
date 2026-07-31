#!/usr/bin/env bash
set -euo pipefail
base_commit=06e30346a48f3dfa54f3c305b7410cb7a4638d30
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
