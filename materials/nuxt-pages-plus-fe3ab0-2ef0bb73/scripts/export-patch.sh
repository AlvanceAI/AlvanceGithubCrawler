#!/usr/bin/env bash
set -euo pipefail
base_commit=2ef0bb73eafae6b6c24b833ad8bc86216919efa2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
