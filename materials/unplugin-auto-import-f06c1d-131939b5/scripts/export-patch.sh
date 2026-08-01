#!/usr/bin/env bash
set -euo pipefail
base_commit=131939b5a0d3d0efa4326b99035a2644ff245bc5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
