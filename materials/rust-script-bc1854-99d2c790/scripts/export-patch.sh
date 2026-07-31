#!/usr/bin/env bash
set -euo pipefail
base_commit=99d2c790b303c1d75de5cd90499800283e4b9681
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
