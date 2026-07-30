#!/usr/bin/env bash
set -euo pipefail
base_commit=7a00f309a5b8d8b2193cfa2ceea77a7be05013a0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
