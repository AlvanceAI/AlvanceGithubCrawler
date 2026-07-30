#!/usr/bin/env bash
set -euo pipefail
base_commit=bfe693f12ccfb324ef49cf4093994cec6bd6754b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
