#!/usr/bin/env bash
set -euo pipefail
base_commit=b1fead52ccda0c497d816696f23f4099c3e8ec1f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
