#!/usr/bin/env bash
set -euo pipefail
base_commit=1ab8739506fe6f7aafc6543dfb2a44e6fb9e2071
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
