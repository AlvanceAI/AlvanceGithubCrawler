#!/usr/bin/env bash
set -euo pipefail
base_commit=6b86cca7457364888032e6ff9c04f2a87fc14cb2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
