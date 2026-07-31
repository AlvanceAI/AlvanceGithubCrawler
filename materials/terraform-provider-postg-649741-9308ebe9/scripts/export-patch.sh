#!/usr/bin/env bash
set -euo pipefail
base_commit=9308ebe9b91aceef89b3a06e2d69c3ef7768a849
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
