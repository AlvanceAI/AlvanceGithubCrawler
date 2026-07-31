#!/usr/bin/env bash
set -euo pipefail
base_commit=3934c9cdf72ac4806f3a2ef77004b62d1e236028
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
