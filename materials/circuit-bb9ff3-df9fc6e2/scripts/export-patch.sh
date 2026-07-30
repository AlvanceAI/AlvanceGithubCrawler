#!/usr/bin/env bash
set -euo pipefail
base_commit=df9fc6e22e7683d17ae5bacd49f3dd241540b90e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
