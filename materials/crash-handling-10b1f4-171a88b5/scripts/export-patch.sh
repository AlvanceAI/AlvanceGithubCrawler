#!/usr/bin/env bash
set -euo pipefail
base_commit=171a88b5a914ffff8607cbe8763d8c4dd59fbd02
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
