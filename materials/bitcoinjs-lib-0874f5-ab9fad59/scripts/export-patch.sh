#!/usr/bin/env bash
set -euo pipefail
base_commit=ab9fad5978bc1f4fb6542d1cde903d4427c3344e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
