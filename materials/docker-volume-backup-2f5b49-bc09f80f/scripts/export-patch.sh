#!/usr/bin/env bash
set -euo pipefail
base_commit=bc09f80fc72b3042c40b6e9a472fe58f39a5872c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
