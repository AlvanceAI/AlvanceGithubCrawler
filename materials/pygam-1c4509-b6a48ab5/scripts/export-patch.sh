#!/usr/bin/env bash
set -euo pipefail
base_commit=b6a48ab5d1ef7df07ce2a34bbe572bca75e83e7d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
