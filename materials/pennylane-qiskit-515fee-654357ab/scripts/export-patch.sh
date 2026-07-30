#!/usr/bin/env bash
set -euo pipefail
base_commit=654357ab7907a485935959869fd4c6d42178b9ba
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
