#!/usr/bin/env bash
set -euo pipefail
base_commit=f4ecbd1bf2fc59281eab848b6cbd1976c434ddac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
