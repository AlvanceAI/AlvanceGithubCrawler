#!/usr/bin/env bash
set -euo pipefail
base_commit=45b6a78e0f9ece585e56c2f9763e707f7642de2e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
