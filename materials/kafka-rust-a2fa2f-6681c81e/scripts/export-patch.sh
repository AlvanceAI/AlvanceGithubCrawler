#!/usr/bin/env bash
set -euo pipefail
base_commit=6681c81e0f7a84547e972ec545f3ed278d2ecfec
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
