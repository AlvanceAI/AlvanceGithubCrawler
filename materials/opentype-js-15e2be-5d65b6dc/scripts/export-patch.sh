#!/usr/bin/env bash
set -euo pipefail
base_commit=5d65b6dcfab5115f90d375f8ba6b7942fdaa0138
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
