#!/usr/bin/env bash
set -euo pipefail
base_commit=a0cb7c50b78028f840b238d8e1c391e0546f2325
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
