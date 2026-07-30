#!/usr/bin/env bash
set -euo pipefail
base_commit=1f60a3f27b4889ee42f5db4076f872df6395b713
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
