#!/usr/bin/env bash
set -euo pipefail
base_commit=f94f1ce26abe3e0346d44740c2c7360ef94ea0ac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
