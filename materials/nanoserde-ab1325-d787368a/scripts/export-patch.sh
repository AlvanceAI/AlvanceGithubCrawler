#!/usr/bin/env bash
set -euo pipefail
base_commit=d787368af9bdf9762e8d46185fe74be09adbef4b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
