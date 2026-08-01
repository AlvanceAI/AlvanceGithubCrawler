#!/usr/bin/env bash
set -euo pipefail
base_commit=2537c7bd9d64af06ed3c1f023e995d081f205da6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
