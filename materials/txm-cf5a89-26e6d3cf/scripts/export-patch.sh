#!/usr/bin/env bash
set -euo pipefail
base_commit=26e6d3cfef4d5d040711f4c49d9147aabd350d4d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
