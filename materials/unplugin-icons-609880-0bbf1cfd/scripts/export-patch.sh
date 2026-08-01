#!/usr/bin/env bash
set -euo pipefail
base_commit=0bbf1cfdb1812a711d3e8b77268b16dab1272ee5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
