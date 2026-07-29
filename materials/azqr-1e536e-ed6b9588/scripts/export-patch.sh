#!/usr/bin/env bash
set -euo pipefail
base_commit=ed6b95888a221c576b53ec39aeb441242112ef4d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
