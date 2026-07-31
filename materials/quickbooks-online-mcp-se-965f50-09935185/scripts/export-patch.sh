#!/usr/bin/env bash
set -euo pipefail
base_commit=099351858ee696dbbeb00dc7ca8e3a86276d86bb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
