#!/usr/bin/env bash
set -euo pipefail
base_commit=40eeccdc29460646af714f1a1e9ab2f76d8e4b20
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
