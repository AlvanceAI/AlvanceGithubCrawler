#!/usr/bin/env bash
set -euo pipefail
base_commit=cd1242c779eef984d532aac3aefbc2ea7fa4c1af
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
