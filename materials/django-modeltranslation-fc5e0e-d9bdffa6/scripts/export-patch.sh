#!/usr/bin/env bash
set -euo pipefail
base_commit=d9bdffa6108ef38db2e203e67a1affa99a7b39b1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
