#!/usr/bin/env bash
set -euo pipefail
base_commit=eaa67f02559c071cbe41b3111e930c154e8ec315
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
