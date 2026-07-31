#!/usr/bin/env bash
set -euo pipefail
base_commit=ace9b634c17c7a72d9323a849fbfbfc2e2b3fb35
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
