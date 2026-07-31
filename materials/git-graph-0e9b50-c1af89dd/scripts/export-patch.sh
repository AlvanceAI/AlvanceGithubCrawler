#!/usr/bin/env bash
set -euo pipefail
base_commit=c1af89dd79be5947d6a86c2b5b80cbbc2689dead
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
