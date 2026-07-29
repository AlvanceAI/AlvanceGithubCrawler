#!/usr/bin/env bash
set -euo pipefail
base_commit=d475ee2cdd311092518983fa98848f53e1fb8b63
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
