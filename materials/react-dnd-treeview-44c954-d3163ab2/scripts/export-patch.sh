#!/usr/bin/env bash
set -euo pipefail
base_commit=d3163ab29d01a8e35d57a8da5ecf945657360189
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
