#!/usr/bin/env bash
set -euo pipefail
base_commit=8ed75e4ca7dc66998265a0cac3d32acd2f167211
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
