#!/usr/bin/env bash
set -euo pipefail
base_commit=42db5690dea199f930a6f08005fe2e4aab10dcc9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
