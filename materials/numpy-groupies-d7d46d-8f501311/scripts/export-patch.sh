#!/usr/bin/env bash
set -euo pipefail
base_commit=8f50131102d7cff0a5376c10c4ec8e54c577be5e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
