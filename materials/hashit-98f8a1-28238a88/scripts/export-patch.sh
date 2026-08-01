#!/usr/bin/env bash
set -euo pipefail
base_commit=28238a88c010b59fde90136967315caf44f35b01
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
