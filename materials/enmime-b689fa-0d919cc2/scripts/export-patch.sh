#!/usr/bin/env bash
set -euo pipefail
base_commit=0d919cc223e9cb6c2d45d6c653e7a64156006351
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
