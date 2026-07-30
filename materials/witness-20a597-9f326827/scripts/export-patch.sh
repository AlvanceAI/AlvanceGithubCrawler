#!/usr/bin/env bash
set -euo pipefail
base_commit=9f32682747f0b12d4b4d01d608b5ee644044e8a5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
