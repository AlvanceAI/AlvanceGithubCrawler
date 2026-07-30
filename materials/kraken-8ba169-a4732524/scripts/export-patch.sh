#!/usr/bin/env bash
set -euo pipefail
base_commit=a4732524b1932af4e5c742cdf12a9a9ba4532148
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
