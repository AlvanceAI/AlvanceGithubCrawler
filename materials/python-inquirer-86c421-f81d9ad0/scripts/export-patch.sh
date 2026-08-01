#!/usr/bin/env bash
set -euo pipefail
base_commit=f81d9ad09797780e8f9195177e4902d5ea51241e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
