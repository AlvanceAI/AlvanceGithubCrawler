#!/usr/bin/env bash
set -euo pipefail
base_commit=f6a8c43d12cc115492221f2082289cfe742e4f66
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
