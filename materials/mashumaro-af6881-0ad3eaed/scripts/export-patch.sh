#!/usr/bin/env bash
set -euo pipefail
base_commit=0ad3eaed34f09e4a361613b607aa78e9a51d9999
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
