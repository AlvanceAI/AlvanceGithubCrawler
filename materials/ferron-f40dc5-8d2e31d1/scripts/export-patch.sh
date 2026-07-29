#!/usr/bin/env bash
set -euo pipefail
base_commit=8d2e31d1f6c771fa78d450cddd1f936b40cd3c21
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
