#!/usr/bin/env bash
set -euo pipefail
base_commit=3aba0a6ffa8995cfc8b244bbde397fbf8f546ae3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
