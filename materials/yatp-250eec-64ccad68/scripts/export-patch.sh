#!/usr/bin/env bash
set -euo pipefail
base_commit=64ccad68f86f06c2cbb5a95fb3258c2c092ecea0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
