#!/usr/bin/env bash
set -euo pipefail
base_commit=43f5e9167cad849701c3307761f897dc9f7a50c5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
