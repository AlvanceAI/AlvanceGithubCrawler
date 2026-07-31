#!/usr/bin/env bash
set -euo pipefail
base_commit=8883990d1eacb9e8c292b7d6301a2e9b97913ce4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
