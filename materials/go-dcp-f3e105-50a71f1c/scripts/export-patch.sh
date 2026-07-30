#!/usr/bin/env bash
set -euo pipefail
base_commit=50a71f1c046aa21f8fa631a90e5a4f29b4dd142f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
