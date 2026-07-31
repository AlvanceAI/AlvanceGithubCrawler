#!/usr/bin/env bash
set -euo pipefail
base_commit=6451cc5d2dc7a6fd495db66c025de9987721f4f4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
