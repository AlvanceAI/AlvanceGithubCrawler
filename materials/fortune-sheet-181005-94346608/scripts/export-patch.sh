#!/usr/bin/env bash
set -euo pipefail
base_commit=94346608877db4747406707a177c4b8f3bacdbf9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
