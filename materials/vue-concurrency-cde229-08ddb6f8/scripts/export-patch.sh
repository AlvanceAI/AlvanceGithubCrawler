#!/usr/bin/env bash
set -euo pipefail
base_commit=08ddb6f87fecb35d5416a8259145459efbda99bc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
