#!/usr/bin/env bash
set -euo pipefail
base_commit=5d1c8bfc21e737c03a3cb14e06b4e472e2275ff1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
