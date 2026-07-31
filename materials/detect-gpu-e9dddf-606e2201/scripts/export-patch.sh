#!/usr/bin/env bash
set -euo pipefail
base_commit=606e22010e790870cc33cd42a9ba356ace608cf3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
