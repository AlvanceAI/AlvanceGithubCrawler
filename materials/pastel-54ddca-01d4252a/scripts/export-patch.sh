#!/usr/bin/env bash
set -euo pipefail
base_commit=01d4252aa794f1331834948f133e75c64532be46
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
