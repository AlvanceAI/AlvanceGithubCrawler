#!/usr/bin/env bash
set -euo pipefail
base_commit=0d2d958f87be99a5fbb7b3d05fd90931d24103f0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
