#!/usr/bin/env bash
set -euo pipefail
base_commit=86dba46a27e8eda83786a2720ca821d3c296d2db
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
