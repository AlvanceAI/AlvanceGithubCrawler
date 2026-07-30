#!/usr/bin/env bash
set -euo pipefail
base_commit=b7daa48cdfdb1a85890faa2b455a22dfd185eb23
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
