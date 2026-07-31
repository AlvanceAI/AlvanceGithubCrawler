#!/usr/bin/env bash
set -euo pipefail
base_commit=236ed3a82d59af3318fd6674e82f0f67629ef205
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
