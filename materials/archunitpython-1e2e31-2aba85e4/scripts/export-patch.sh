#!/usr/bin/env bash
set -euo pipefail
base_commit=2aba85e44fcc8a95334efb54c3cc25b1508732c6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
