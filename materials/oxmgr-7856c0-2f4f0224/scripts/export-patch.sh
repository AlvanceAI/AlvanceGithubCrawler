#!/usr/bin/env bash
set -euo pipefail
base_commit=2f4f0224a50abd7b98976990f90b3e8fda3215bd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
