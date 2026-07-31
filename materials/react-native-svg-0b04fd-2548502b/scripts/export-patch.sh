#!/usr/bin/env bash
set -euo pipefail
base_commit=2548502b31fadcd85972a15fb4d964154b5971ef
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
