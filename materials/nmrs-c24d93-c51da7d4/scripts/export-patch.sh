#!/usr/bin/env bash
set -euo pipefail
base_commit=c51da7d4eadb5dabf987a31ce5595d17738e5915
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
