#!/usr/bin/env bash
set -euo pipefail
base_commit=2045e714610fdab6c659c937154732ca28f65213
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
