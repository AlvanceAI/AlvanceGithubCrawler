#!/usr/bin/env bash
set -euo pipefail
base_commit=f5d248c4db462e626fd91ea2d383a09fe42102c0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
