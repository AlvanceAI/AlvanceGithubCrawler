#!/usr/bin/env bash
set -euo pipefail
base_commit=e13acb5c9ef9d5c50cf80c8844f1713dcaff32a3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
