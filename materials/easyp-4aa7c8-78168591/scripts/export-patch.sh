#!/usr/bin/env bash
set -euo pipefail
base_commit=781685913af1898c5cd69b739571f8c2b3925466
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
