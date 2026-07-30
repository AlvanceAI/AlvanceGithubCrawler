#!/usr/bin/env bash
set -euo pipefail
base_commit=7ceb9154052e9bf5944be78e0e08f2d1b8eaae9b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
