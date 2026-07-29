#!/usr/bin/env bash
set -euo pipefail
base_commit=4ade611e0738be345a6aa732aefcd36a64793fb3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
