#!/usr/bin/env bash
set -euo pipefail
base_commit=305098790fddc6dc415cb9a2c220e6ad9b170c41
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
