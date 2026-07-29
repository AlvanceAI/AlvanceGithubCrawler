#!/usr/bin/env bash
set -euo pipefail
base_commit=22f719a4063610bdc6ff819a0a6084e344308a0f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
