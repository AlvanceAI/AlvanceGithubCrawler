#!/usr/bin/env bash
set -euo pipefail
base_commit=03f11113166ee96aa6594d8c12742dc1419903d1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
