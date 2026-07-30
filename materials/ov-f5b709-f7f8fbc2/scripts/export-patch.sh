#!/usr/bin/env bash
set -euo pipefail
base_commit=f7f8fbc28ae8e36b0c9547088ae25e936b6dd7a0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
