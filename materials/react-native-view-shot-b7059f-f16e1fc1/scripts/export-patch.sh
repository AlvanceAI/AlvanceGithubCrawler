#!/usr/bin/env bash
set -euo pipefail
base_commit=f16e1fc13d0f3c735b78928f753037a6490d4ae1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
