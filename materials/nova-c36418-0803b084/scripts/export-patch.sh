#!/usr/bin/env bash
set -euo pipefail
base_commit=0803b0840d990bbf6518951899fcf8b948acc971
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
