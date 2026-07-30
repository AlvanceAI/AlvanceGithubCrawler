#!/usr/bin/env bash
set -euo pipefail
base_commit=70f72bee542ae49efebb8d2106bde64f84f02a43
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
