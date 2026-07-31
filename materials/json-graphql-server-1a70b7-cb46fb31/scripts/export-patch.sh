#!/usr/bin/env bash
set -euo pipefail
base_commit=cb46fb31256a2c72ee5a495c000ad817c1e25885
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
