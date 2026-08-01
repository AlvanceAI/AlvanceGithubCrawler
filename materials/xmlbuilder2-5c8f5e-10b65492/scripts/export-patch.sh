#!/usr/bin/env bash
set -euo pipefail
base_commit=10b65492d4c47a3a7c88e430be5b1d7bbd0ac85a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
