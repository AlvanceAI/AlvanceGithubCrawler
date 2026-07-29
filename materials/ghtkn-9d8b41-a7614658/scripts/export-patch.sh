#!/usr/bin/env bash
set -euo pipefail
base_commit=a7614658864ac00c7e80f5f76d2aaa4b5ad66b72
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
