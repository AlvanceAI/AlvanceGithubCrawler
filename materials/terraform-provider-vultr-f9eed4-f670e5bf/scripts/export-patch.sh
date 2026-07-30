#!/usr/bin/env bash
set -euo pipefail
base_commit=f670e5bf534cd8c51300380b344050c076ff94c4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
