#!/usr/bin/env bash
set -euo pipefail
base_commit=fc2c853cf7491c49147170d9f442eeb8d7589c2e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
