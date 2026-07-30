#!/usr/bin/env bash
set -euo pipefail
base_commit=8c3305a470fefc9098f9b54c0905b1cf1e83d764
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
