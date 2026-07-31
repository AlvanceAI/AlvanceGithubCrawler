#!/usr/bin/env bash
set -euo pipefail
base_commit=008b0ed9cae7d5d5b0c72e23c84836c5b2f0338b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
