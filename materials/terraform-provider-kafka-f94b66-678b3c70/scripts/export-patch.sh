#!/usr/bin/env bash
set -euo pipefail
base_commit=678b3c706c77585a2d866d1b1469a2235c2e98db
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
