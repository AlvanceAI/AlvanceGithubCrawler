#!/usr/bin/env bash
set -euo pipefail
base_commit=68759b97965776fdc9571485656f87088088b741
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
