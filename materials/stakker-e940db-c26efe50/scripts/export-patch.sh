#!/usr/bin/env bash
set -euo pipefail
base_commit=c26efe5072eb0dfb19d5b59e4d8159fee91c4b60
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
