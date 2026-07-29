#!/usr/bin/env bash
set -euo pipefail
base_commit=752f842e39c8ba9e2e12eda4af4a7c9a14126dc3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
