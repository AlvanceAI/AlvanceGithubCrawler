#!/usr/bin/env bash
set -euo pipefail
base_commit=68b772d142e0512adb201bd215f99e993dd9102a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
