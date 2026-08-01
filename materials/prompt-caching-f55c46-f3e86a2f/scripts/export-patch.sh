#!/usr/bin/env bash
set -euo pipefail
base_commit=f3e86a2f80229a3e04d037195e08afcdfd1b1d12
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
