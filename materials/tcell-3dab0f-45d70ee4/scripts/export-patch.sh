#!/usr/bin/env bash
set -euo pipefail
base_commit=45d70ee4abf221813842b88aba8abae08a992f2f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
