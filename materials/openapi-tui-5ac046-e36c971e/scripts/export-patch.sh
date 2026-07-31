#!/usr/bin/env bash
set -euo pipefail
base_commit=e36c971e0d5086eda21b8fe9815511f5d3ae4b06
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
