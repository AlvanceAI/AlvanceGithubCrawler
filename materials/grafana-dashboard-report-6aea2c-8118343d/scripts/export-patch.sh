#!/usr/bin/env bash
set -euo pipefail
base_commit=8118343db326d26affff2f270ae5643da677f14d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
