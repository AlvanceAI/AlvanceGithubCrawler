#!/usr/bin/env bash
set -euo pipefail
base_commit=9018e8e2669efaf06d0157d315f2d14ea1e36d24
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
