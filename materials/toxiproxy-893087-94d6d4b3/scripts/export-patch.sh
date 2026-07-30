#!/usr/bin/env bash
set -euo pipefail
base_commit=94d6d4b3c385e48534622b138da61e95014196d5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
