#!/usr/bin/env bash
set -euo pipefail
base_commit=cbf234e54acbac9636d56b28efd573560e30a608
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
