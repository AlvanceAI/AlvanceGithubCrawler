#!/usr/bin/env bash
set -euo pipefail
base_commit=6a92e54c748766973add4b8c153fcc85738d2d89
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
