#!/usr/bin/env bash
set -euo pipefail
base_commit=7cb742b27561de7e397ca43f9c74e4f514dfbe07
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
