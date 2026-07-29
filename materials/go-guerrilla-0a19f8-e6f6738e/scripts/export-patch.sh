#!/usr/bin/env bash
set -euo pipefail
base_commit=e6f6738ef3ecbba55e637b6223c9366c9813f59f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
