#!/usr/bin/env bash
set -euo pipefail
base_commit=2057dab9914c82c5dec0625bc801c41244b8d353
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
