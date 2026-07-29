#!/usr/bin/env bash
set -euo pipefail
base_commit=456fae9d0464944b946a288aed152dbb0c369a76
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
