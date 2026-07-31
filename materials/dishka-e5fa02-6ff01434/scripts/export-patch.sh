#!/usr/bin/env bash
set -euo pipefail
base_commit=6ff01434ba4e3cc93d1dab86e79c5bf06d105bfe
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
