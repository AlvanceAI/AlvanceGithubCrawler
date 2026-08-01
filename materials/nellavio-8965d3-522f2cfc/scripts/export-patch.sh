#!/usr/bin/env bash
set -euo pipefail
base_commit=522f2cfc78567c7b64f94e8c1f7da65ea4e02551
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
