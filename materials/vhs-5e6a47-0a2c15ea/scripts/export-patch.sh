#!/usr/bin/env bash
set -euo pipefail
base_commit=0a2c15eab702062a2044816729ba2c356ab47687
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
