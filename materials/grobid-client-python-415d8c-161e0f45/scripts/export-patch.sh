#!/usr/bin/env bash
set -euo pipefail
base_commit=161e0f45189c8592b2e2c58e9638cc6218bc75fb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
