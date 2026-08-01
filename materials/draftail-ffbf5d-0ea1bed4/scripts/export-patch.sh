#!/usr/bin/env bash
set -euo pipefail
base_commit=0ea1bed4510dd26e4e784e06afce2f8b831a7ad7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
