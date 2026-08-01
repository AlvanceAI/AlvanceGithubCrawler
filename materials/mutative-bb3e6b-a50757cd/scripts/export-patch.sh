#!/usr/bin/env bash
set -euo pipefail
base_commit=a50757cdae465034f8370a886cae32626d6c317e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
