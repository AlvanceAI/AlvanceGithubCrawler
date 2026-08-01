#!/usr/bin/env bash
set -euo pipefail
base_commit=312e27333e14f841b95bf4f2b205a856b4a4c370
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
