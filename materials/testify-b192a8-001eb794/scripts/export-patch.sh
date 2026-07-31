#!/usr/bin/env bash
set -euo pipefail
base_commit=001eb7946baf451879253643e4ce4b38eaa0d4a7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
