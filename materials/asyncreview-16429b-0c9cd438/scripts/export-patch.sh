#!/usr/bin/env bash
set -euo pipefail
base_commit=0c9cd438b1682befc4f3e56b150f9840f1baf745
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
