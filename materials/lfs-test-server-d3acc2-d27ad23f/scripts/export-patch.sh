#!/usr/bin/env bash
set -euo pipefail
base_commit=d27ad23fddc1949ecd9a4ba6a3d074bc6a567084
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
