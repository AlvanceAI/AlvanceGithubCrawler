#!/usr/bin/env bash
set -euo pipefail
base_commit=72017bd9139b8076de3733939ac2465dbd82b48a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
