#!/usr/bin/env bash
set -euo pipefail
base_commit=551a674eb855d5debcd2d0262e93e22ac1feed62
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
