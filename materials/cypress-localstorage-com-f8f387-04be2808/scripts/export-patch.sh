#!/usr/bin/env bash
set -euo pipefail
base_commit=04be2808ac64ed870fb55ed03bd75174c2980ee8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
