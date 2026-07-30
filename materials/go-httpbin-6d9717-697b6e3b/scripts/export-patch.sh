#!/usr/bin/env bash
set -euo pipefail
base_commit=697b6e3b326edfd8915a3b1c36c4a43f367ea3ac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
