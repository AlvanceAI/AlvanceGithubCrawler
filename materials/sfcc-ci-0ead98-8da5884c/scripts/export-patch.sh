#!/usr/bin/env bash
set -euo pipefail
base_commit=8da5884c2de46cfaa50d0bbeaf3c6342b9c3c13b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
