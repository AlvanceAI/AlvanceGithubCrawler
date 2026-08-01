#!/usr/bin/env bash
set -euo pipefail
base_commit=8ce74848929d1c46ac4c5da5fad0e43596e45ffa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
