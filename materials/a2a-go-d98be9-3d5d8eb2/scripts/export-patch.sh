#!/usr/bin/env bash
set -euo pipefail
base_commit=3d5d8eb2ff95429c7029d7547fd43eab2f181a7f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
