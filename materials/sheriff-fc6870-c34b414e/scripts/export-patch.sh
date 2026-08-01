#!/usr/bin/env bash
set -euo pipefail
base_commit=c34b414e5e4e00632b5174ecaf875e18275f06b2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
