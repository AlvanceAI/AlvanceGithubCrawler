#!/usr/bin/env bash
set -euo pipefail
base_commit=5e141933554a0b74e7341841f318be21e895339c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
