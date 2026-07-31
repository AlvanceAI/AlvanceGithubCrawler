#!/usr/bin/env bash
set -euo pipefail
base_commit=c6fa40c42bdec242aae64c8a5e620e2200d8a736
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
