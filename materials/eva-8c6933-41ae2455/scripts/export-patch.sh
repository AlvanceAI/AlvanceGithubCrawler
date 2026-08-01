#!/usr/bin/env bash
set -euo pipefail
base_commit=41ae2455085c10978c5d93be4e6b139682396eb0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
