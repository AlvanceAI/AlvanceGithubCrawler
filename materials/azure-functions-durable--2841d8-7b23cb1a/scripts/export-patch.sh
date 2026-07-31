#!/usr/bin/env bash
set -euo pipefail
base_commit=7b23cb1a17f3ee6d421b8cb5c239f80ecb587a54
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
