#!/usr/bin/env bash
set -euo pipefail
base_commit=62e0594d2dd56fa480c8084cb807efddb340400a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
