#!/usr/bin/env bash
set -euo pipefail
base_commit=8a763a0a1e92317b4822a9ea1cfaaf150b036f12
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
