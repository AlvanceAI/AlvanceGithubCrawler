#!/usr/bin/env bash
set -euo pipefail
base_commit=7ddde34a09ad6e5432e27b4bea6171c39edb4792
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
