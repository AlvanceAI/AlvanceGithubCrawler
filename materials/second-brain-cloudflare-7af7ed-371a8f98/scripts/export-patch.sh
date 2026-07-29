#!/usr/bin/env bash
set -euo pipefail
base_commit=371a8f987b2e4e8d95fc60d20580fb4757877641
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
