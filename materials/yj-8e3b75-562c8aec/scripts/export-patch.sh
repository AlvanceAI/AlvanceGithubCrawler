#!/usr/bin/env bash
set -euo pipefail
base_commit=562c8aec6fb4d25626f38eae0c1f1374e54faa57
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
