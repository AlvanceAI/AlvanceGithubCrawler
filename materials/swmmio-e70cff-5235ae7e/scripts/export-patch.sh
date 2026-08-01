#!/usr/bin/env bash
set -euo pipefail
base_commit=5235ae7e7daae61291734daf4d6b78e18fd445e9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
