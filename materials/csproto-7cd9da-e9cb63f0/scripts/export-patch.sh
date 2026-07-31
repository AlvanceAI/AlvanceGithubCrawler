#!/usr/bin/env bash
set -euo pipefail
base_commit=e9cb63f0641def4dd562ff11b4cc3e19f961dc90
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
