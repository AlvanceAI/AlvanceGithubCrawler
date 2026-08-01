#!/usr/bin/env bash
set -euo pipefail
base_commit=d135459ef6c1fdd005f28c6e2cf7915e8fb8d0e1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
