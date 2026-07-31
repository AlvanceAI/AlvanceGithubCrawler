#!/usr/bin/env bash
set -euo pipefail
base_commit=98a2862d99cdd259c5fd9be3d4784d01b1cfcf95
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
