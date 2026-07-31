#!/usr/bin/env bash
set -euo pipefail
base_commit=e3e3f2331d771e59b871a08c8ea23f8880011cca
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
