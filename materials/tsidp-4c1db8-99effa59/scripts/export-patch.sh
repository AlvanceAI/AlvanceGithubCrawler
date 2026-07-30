#!/usr/bin/env bash
set -euo pipefail
base_commit=99effa593a177e55f6e8ebd64041c4da602f9807
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
