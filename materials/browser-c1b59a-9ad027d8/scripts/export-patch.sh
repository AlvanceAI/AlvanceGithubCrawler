#!/usr/bin/env bash
set -euo pipefail
base_commit=9ad027d88d4533bd6d29f9d8d7e517e23cd361ff
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
