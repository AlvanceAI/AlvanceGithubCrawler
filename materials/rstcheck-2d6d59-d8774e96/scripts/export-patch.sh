#!/usr/bin/env bash
set -euo pipefail
base_commit=d8774e96810795967ed9603f445b4e751e7b313f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
