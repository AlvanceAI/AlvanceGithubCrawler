#!/usr/bin/env bash
set -euo pipefail
base_commit=4850de716d3bdf5a1567c99e5776164a8fe8bfea
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
