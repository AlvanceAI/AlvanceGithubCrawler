#!/usr/bin/env bash
set -euo pipefail
base_commit=9e62719b740ae3306ad987657bcd63d0af1858f7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
