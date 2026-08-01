#!/usr/bin/env bash
set -euo pipefail
base_commit=749e602a1e19dfc194750a543d3db40ca8820a33
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
