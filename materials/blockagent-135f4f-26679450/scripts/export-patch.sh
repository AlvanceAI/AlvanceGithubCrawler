#!/usr/bin/env bash
set -euo pipefail
base_commit=26679450caeb27b19e9bde2015222f540692619a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
