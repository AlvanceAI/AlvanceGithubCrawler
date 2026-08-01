#!/usr/bin/env bash
set -euo pipefail
base_commit=7695aaa104fd54fa0116b49a0a391c135466aec2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
