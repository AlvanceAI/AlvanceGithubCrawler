#!/usr/bin/env bash
set -euo pipefail
base_commit=fcff951833435579dddd43b2f43cf6531ce62223
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
