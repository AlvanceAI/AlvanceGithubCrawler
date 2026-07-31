#!/usr/bin/env bash
set -euo pipefail
base_commit=d74024df774054fa411a9d5cca6013ce91d26208
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
