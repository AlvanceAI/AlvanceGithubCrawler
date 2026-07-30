#!/usr/bin/env bash
set -euo pipefail
base_commit=bda3903d384fcb8d06e19ea85bdad5f7c211ca0c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
