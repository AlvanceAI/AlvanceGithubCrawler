#!/usr/bin/env bash
set -euo pipefail
base_commit=7d9fa54a58aa48933377575ffa7ba390a58f24a6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
