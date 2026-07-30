#!/usr/bin/env bash
set -euo pipefail
base_commit=8690112733ef954d997243926f5521a809ad6e88
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
