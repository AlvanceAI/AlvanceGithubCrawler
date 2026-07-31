#!/usr/bin/env bash
set -euo pipefail
base_commit=e55de0bdf3a8bf87019dd197504ec27568106a2c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
