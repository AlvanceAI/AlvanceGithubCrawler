#!/usr/bin/env bash
set -euo pipefail
base_commit=716d8b5d0221558f944b5a078dbbcca8572534fb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
