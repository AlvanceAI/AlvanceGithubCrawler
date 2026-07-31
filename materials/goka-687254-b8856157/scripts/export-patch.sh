#!/usr/bin/env bash
set -euo pipefail
base_commit=b8856157710989eeaa37832bfa8fe12aaf3f8b87
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
