#!/usr/bin/env bash
set -euo pipefail
base_commit=d854b7e0e2d39884e7ab42c5ab0bce2830a3687c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
