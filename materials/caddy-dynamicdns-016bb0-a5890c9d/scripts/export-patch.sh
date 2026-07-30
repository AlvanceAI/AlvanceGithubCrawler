#!/usr/bin/env bash
set -euo pipefail
base_commit=a5890c9df68cb7ed603f552a624f6123a5fad2ff
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
