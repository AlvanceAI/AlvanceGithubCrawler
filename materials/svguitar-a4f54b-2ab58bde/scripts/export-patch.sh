#!/usr/bin/env bash
set -euo pipefail
base_commit=2ab58bdeb8797e61b0ed10f2945d296bacb23c45
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
