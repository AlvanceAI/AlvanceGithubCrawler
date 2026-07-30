#!/usr/bin/env bash
set -euo pipefail
base_commit=50e613bc9467af6ae08c528085857bca3a0397f3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
