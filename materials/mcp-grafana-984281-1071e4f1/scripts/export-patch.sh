#!/usr/bin/env bash
set -euo pipefail
base_commit=1071e4f1f9b2e42260570a8f85956e9b7365e322
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
