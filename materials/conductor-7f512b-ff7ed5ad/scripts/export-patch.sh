#!/usr/bin/env bash
set -euo pipefail
base_commit=ff7ed5ad305d4342d42b1da230affe111ce86927
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
