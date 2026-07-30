#!/usr/bin/env bash
set -euo pipefail
base_commit=e0f442238e74050cbd686355a5c2af0115000432
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
