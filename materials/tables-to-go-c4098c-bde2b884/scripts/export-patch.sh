#!/usr/bin/env bash
set -euo pipefail
base_commit=bde2b88402a8181782f9ce5e9ee0c0331cf60352
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
