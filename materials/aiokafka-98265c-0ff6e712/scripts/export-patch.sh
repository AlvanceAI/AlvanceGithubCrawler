#!/usr/bin/env bash
set -euo pipefail
base_commit=0ff6e7123a887fe254bb06b5d1f7b2742e6c4274
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
