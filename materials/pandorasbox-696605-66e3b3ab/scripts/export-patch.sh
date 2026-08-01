#!/usr/bin/env bash
set -euo pipefail
base_commit=66e3b3abd6ccde2693623560e92e287f6e8f8b48
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
