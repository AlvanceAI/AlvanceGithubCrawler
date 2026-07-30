#!/usr/bin/env bash
set -euo pipefail
base_commit=2565bbef9222fda044a827e88f9f64411f54ddde
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
