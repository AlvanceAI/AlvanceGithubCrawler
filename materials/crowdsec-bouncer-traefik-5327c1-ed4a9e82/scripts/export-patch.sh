#!/usr/bin/env bash
set -euo pipefail
base_commit=ed4a9e82628a957824d08b6d08273698b9a246b2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
