#!/usr/bin/env bash
set -euo pipefail
base_commit=12cb1375c78063b01080308b554b3a87c272e36d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
