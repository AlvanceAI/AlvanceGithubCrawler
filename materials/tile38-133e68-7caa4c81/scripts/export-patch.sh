#!/usr/bin/env bash
set -euo pipefail
base_commit=7caa4c810ce77e8dfb30d4776cae8a68f9a2e209
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
