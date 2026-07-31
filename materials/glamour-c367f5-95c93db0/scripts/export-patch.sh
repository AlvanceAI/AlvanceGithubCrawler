#!/usr/bin/env bash
set -euo pipefail
base_commit=95c93db04489cebf252ec856584445c7e85ee276
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
