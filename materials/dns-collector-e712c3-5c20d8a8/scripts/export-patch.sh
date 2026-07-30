#!/usr/bin/env bash
set -euo pipefail
base_commit=5c20d8a88ac0ca33c6e2ff4cb01af292a88dc2d8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
