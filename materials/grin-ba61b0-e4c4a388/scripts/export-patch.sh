#!/usr/bin/env bash
set -euo pipefail
base_commit=e4c4a38825c2dd3a822d7cdbe8bd4cd6f390e380
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
