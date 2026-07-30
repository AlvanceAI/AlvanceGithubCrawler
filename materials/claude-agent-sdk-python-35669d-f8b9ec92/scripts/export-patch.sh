#!/usr/bin/env bash
set -euo pipefail
base_commit=f8b9ec923982082a02c485924e0f60367949c3a1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
