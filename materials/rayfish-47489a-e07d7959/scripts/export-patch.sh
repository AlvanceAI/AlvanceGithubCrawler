#!/usr/bin/env bash
set -euo pipefail
base_commit=e07d79593c52271c8110f4f271576daa3d34d8d7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
