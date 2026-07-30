#!/usr/bin/env bash
set -euo pipefail
base_commit=7dfc5fbfbc7d66bfd613454288ccf42f339d7a3a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
