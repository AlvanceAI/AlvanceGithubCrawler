#!/usr/bin/env bash
set -euo pipefail
base_commit=891a6ff3772118412a9ae42187c4152fcb4fc181
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
