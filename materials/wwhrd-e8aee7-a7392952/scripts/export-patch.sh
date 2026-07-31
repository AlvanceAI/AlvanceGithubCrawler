#!/usr/bin/env bash
set -euo pipefail
base_commit=a73929525483c58cbd0b2623895527791e440205
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
