#!/usr/bin/env bash
set -euo pipefail
base_commit=5e896fb3398cc86acd735d170fb758a02528b70e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
