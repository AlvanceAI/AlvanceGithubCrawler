#!/usr/bin/env bash
set -euo pipefail
base_commit=2009aff0284fe4342c6c0ca62044ff55829be597
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
