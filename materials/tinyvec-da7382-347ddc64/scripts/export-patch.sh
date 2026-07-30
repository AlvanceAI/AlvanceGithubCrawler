#!/usr/bin/env bash
set -euo pipefail
base_commit=347ddc6463159eec38d3758a8881a22f44d50373
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
