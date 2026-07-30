#!/usr/bin/env bash
set -euo pipefail
base_commit=3febb4cee5ec81fd8e8220192eeac3103d2c55fb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
