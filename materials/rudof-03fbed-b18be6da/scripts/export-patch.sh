#!/usr/bin/env bash
set -euo pipefail
base_commit=b18be6dadfbb461816a578335ed56edba239f704
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
