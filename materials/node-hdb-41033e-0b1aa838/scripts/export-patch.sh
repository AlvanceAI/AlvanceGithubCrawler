#!/usr/bin/env bash
set -euo pipefail
base_commit=0b1aa8384b3da6c7dd7352dde5ad6f0e5205217f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
