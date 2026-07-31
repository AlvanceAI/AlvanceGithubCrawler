#!/usr/bin/env bash
set -euo pipefail
base_commit=4a6006f6e78daedf28e160ee3f3745c3f14505d4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
