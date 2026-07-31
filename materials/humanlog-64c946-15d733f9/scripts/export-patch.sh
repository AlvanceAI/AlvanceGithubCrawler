#!/usr/bin/env bash
set -euo pipefail
base_commit=15d733f9b72b911dca5de9c1e6b2e110cf57589e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
