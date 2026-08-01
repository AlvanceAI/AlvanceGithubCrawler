#!/usr/bin/env bash
set -euo pipefail
base_commit=2a672c523b4cb46a6dc7d04ab05fa0f4be72aade
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
