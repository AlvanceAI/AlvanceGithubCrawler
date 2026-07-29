#!/usr/bin/env bash
set -euo pipefail
base_commit=54cfa52e744040578f26ae80b08cf5ef45213cdd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
