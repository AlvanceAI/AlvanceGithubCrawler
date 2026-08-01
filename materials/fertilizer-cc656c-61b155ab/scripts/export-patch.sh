#!/usr/bin/env bash
set -euo pipefail
base_commit=61b155ab879cba51529005636dcee76c0c86c884
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
