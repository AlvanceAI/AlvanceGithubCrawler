#!/usr/bin/env bash
set -euo pipefail
base_commit=fa142caffd7d00288ae96c180697acdf6a28e916
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
