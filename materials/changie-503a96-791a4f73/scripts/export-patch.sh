#!/usr/bin/env bash
set -euo pipefail
base_commit=791a4f73e5ed4b80384f2a2e2c66d14b7eb0094b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
