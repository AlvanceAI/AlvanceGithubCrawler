#!/usr/bin/env bash
set -euo pipefail
base_commit=d7dc356679f393e767ef11f6c9eddfb0240e89e6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
