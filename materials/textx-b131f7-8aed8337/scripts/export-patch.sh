#!/usr/bin/env bash
set -euo pipefail
base_commit=8aed833726501d8772d0e23ddbdd2a41b3cf9154
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
