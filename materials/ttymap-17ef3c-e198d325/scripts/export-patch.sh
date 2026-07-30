#!/usr/bin/env bash
set -euo pipefail
base_commit=e198d3255237a4e51f380583444c6058a3abe078
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
