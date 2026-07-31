#!/usr/bin/env bash
set -euo pipefail
base_commit=d47299dbc15e393b4dc3f97e90fdc39bc3079e66
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
