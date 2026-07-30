#!/usr/bin/env bash
set -euo pipefail
base_commit=27d4f11b7626f2640810ad63749771a46937d3c6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
