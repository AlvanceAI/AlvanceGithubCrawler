#!/usr/bin/env bash
set -euo pipefail
base_commit=198225eaac0c8be4aaa1962d5a9a075d3a6fd062
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
