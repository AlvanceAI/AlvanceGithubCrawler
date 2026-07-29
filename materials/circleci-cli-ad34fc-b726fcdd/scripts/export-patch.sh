#!/usr/bin/env bash
set -euo pipefail
base_commit=b726fcdd00d9ec404c63c85950c9e190b1b5ad68
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
