#!/usr/bin/env bash
set -euo pipefail
base_commit=e3f95e64d40419d779321fab128d7d32a559a56b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
