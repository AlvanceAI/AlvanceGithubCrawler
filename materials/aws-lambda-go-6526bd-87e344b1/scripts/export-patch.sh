#!/usr/bin/env bash
set -euo pipefail
base_commit=87e344b1d4de6b5378079a153603e22ec1c77aa1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
