#!/usr/bin/env bash
set -euo pipefail
base_commit=ab90b516419f154407def759491d8c5deda93115
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
