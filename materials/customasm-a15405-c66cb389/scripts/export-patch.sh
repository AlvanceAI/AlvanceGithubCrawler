#!/usr/bin/env bash
set -euo pipefail
base_commit=c66cb389e7af95ad612520d4766bcb09adfea948
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
