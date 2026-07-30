#!/usr/bin/env bash
set -euo pipefail
base_commit=1f9614905cc2c2337bfaa39ce6c24f0ba6bd5e2e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
