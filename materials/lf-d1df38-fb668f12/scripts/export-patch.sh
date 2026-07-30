#!/usr/bin/env bash
set -euo pipefail
base_commit=fb668f12be74e98c48ab2d31c3d4aa1bfeb18beb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
