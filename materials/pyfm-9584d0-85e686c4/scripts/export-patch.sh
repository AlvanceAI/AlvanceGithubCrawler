#!/usr/bin/env bash
set -euo pipefail
base_commit=85e686c49f966f424f08dbcacc9ed6ceab6603ea
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
