#!/usr/bin/env bash
set -euo pipefail
base_commit=4f616656692d8f14722ce383d3e15d1c8d313f90
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
