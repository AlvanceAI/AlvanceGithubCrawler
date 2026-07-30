#!/usr/bin/env bash
set -euo pipefail
base_commit=01a92a0410bbedf353030fcc5a686d00916ea417
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
