#!/usr/bin/env bash
set -euo pipefail
base_commit=747814f7d5fbab872df3b02f070c165b91bde062
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
