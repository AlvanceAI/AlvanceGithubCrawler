#!/usr/bin/env bash
set -euo pipefail
base_commit=74e069ce2cd8bf97d879596b1641f0f19e9b2a7e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
