#!/usr/bin/env bash
set -euo pipefail
base_commit=f87ea8dbde3de85f55c5b1d06e5d46edc85390d1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
