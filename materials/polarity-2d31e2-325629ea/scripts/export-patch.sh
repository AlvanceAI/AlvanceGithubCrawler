#!/usr/bin/env bash
set -euo pipefail
base_commit=325629ea33fd25905b76f66d502a26dbf5dcc2a9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
