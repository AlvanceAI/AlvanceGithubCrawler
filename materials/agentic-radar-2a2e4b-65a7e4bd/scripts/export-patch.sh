#!/usr/bin/env bash
set -euo pipefail
base_commit=65a7e4bd01e2034c7cb52e9620eeed287688cc53
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
