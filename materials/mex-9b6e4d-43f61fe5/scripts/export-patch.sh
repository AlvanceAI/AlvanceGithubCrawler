#!/usr/bin/env bash
set -euo pipefail
base_commit=43f61fe586095448e681c74c22c5df2e24c79d5b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
