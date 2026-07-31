#!/usr/bin/env bash
set -euo pipefail
base_commit=8bcfe382975533c597b01e0adfb1a1b6e36d5efb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
