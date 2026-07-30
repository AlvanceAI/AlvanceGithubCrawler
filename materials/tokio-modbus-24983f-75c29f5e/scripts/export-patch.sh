#!/usr/bin/env bash
set -euo pipefail
base_commit=75c29f5e96584fd11b95e8142f71e340a5aa9ebc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
