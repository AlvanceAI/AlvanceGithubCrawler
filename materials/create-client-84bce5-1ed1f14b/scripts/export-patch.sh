#!/usr/bin/env bash
set -euo pipefail
base_commit=1ed1f14b3af00e40b2178f3ae4391d227c32ce2e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
