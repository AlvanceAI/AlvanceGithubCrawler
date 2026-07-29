#!/usr/bin/env bash
set -euo pipefail
base_commit=0fbdf8f8f1cab7571a4e783b8908a3687208e5b4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
