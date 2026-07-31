#!/usr/bin/env bash
set -euo pipefail
base_commit=2b71097772ce928cf26695ee1873093e2ced00d1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
