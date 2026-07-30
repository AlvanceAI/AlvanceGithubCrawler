#!/usr/bin/env bash
set -euo pipefail
base_commit=a7e56da528d61d9dc5eadfcf0833960c5257167e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
