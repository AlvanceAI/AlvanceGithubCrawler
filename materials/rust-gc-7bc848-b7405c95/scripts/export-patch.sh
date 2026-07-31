#!/usr/bin/env bash
set -euo pipefail
base_commit=b7405c95a1956e930d8e5a26f6b68d7077f5b6f7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
