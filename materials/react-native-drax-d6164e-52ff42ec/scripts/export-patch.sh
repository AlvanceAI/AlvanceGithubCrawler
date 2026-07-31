#!/usr/bin/env bash
set -euo pipefail
base_commit=52ff42ec49e84b7ff72808b66c7c75b30978240c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
