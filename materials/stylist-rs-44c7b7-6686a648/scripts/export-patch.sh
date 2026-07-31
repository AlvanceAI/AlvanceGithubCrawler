#!/usr/bin/env bash
set -euo pipefail
base_commit=6686a648b4ac954b9e1900746ea0eac7657cfa96
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
