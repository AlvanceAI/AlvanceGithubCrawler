#!/usr/bin/env bash
set -euo pipefail
base_commit=1b32658519d1f35cd3c4345bb9ced3ba6881bb56
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
