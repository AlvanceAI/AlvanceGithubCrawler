#!/usr/bin/env bash
set -euo pipefail
base_commit=9d0e3574f206a9576b94f3b2aa2527ab419d0390
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
