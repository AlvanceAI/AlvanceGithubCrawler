#!/usr/bin/env bash
set -euo pipefail
base_commit=242670a575c37cab6f74e778949417ba1470c8ba
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
