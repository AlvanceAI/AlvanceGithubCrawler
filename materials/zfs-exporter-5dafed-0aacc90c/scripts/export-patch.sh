#!/usr/bin/env bash
set -euo pipefail
base_commit=0aacc90c6759d8420311fe9b0c21e6058092eae7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
