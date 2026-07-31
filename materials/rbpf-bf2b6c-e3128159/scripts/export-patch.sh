#!/usr/bin/env bash
set -euo pipefail
base_commit=e3128159a7df1207104723b25ebe4ea6b172a677
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
