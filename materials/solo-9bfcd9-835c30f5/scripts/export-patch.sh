#!/usr/bin/env bash
set -euo pipefail
base_commit=835c30f5ce8132dceab5e8da8f8acae94408d284
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
