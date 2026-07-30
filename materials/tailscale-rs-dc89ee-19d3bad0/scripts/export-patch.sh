#!/usr/bin/env bash
set -euo pipefail
base_commit=19d3bad00a7442cfab57f58cbe56ccd7a206c82d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
