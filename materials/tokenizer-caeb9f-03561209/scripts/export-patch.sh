#!/usr/bin/env bash
set -euo pipefail
base_commit=0356120930240678069d72e57a2762d7295e099b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
