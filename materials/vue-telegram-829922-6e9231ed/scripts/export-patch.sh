#!/usr/bin/env bash
set -euo pipefail
base_commit=6e9231ed2348c65f3b6e7a526d9db4b3d9958431
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
