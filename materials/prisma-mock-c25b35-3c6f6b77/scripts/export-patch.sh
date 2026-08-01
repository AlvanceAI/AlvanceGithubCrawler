#!/usr/bin/env bash
set -euo pipefail
base_commit=3c6f6b77d23aa17a39c698d86033da252fb8d683
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
