#!/usr/bin/env bash
set -euo pipefail
base_commit=bd3ade99c1f6d1fbd0f31866153e2d155e7b75ab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
