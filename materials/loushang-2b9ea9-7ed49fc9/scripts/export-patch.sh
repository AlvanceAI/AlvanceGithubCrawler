#!/usr/bin/env bash
set -euo pipefail
base_commit=7ed49fc9b26efcc2d42a6ee1f163c042f4b7e55f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
