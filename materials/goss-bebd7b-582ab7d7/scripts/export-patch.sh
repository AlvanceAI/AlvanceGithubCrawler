#!/usr/bin/env bash
set -euo pipefail
base_commit=582ab7d72d981dda0be06056be4b4bfa0184b7e0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
