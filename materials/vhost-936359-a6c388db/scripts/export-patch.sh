#!/usr/bin/env bash
set -euo pipefail
base_commit=a6c388db1870d52cbd8ebb5c9a0b115ae68b1dfd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
