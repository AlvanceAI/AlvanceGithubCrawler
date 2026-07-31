#!/usr/bin/env bash
set -euo pipefail
base_commit=90e1bc427c6efc81f94acbe6c8bce43616f1c417
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
