#!/usr/bin/env bash
set -euo pipefail
base_commit=790aacbe9bc378c11c706dffb4d5dfadc1861778
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
