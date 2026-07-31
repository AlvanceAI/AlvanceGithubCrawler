#!/usr/bin/env bash
set -euo pipefail
base_commit=d4af02aacd9a9a016e1389ec71f8a3cc7057b10c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
