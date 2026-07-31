#!/usr/bin/env bash
set -euo pipefail
base_commit=521f1850288386fa7276aff66bab2fa289ec80e6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
