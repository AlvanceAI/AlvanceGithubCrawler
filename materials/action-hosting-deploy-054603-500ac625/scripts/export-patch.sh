#!/usr/bin/env bash
set -euo pipefail
base_commit=500ac625ca2dd40cbd15f7659af953801858032a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
