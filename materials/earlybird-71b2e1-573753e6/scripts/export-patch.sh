#!/usr/bin/env bash
set -euo pipefail
base_commit=573753e6f39a02293d4a250878e66664aefa674a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
