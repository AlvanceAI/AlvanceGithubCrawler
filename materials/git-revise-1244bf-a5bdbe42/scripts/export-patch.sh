#!/usr/bin/env bash
set -euo pipefail
base_commit=a5bdbe420521a7784dd16c8f22b374b2f1d2d167
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
