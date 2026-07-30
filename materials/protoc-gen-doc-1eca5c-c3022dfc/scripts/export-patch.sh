#!/usr/bin/env bash
set -euo pipefail
base_commit=c3022dfc79202ffcac753a2f9007103e9d975e2c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
