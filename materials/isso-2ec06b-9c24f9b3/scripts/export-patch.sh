#!/usr/bin/env bash
set -euo pipefail
base_commit=9c24f9b3d9f259cff84b67e50875e6137b459ef7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
