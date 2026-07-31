#!/usr/bin/env bash
set -euo pipefail
base_commit=f678162af201cba391c9bf759b429dee5ad5c0bc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
