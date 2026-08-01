#!/usr/bin/env bash
set -euo pipefail
base_commit=3ecb10381bda8b78f8d8160c0ec6b54a7dc3afdf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
