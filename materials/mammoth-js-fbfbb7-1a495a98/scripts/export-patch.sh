#!/usr/bin/env bash
set -euo pipefail
base_commit=1a495a98856180e25d3b166b51319b165e0ce348
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
