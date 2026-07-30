#!/usr/bin/env bash
set -euo pipefail
base_commit=c3dd90c20c1d9b791c07f41cba736462e5cdedd0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
