#!/usr/bin/env bash
set -euo pipefail
base_commit=832603bbf484165d0629339462a2ad364522e564
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
