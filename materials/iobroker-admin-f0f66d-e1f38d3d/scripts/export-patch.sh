#!/usr/bin/env bash
set -euo pipefail
base_commit=e1f38d3d4c53df6efddd4e7373f984317a02e31b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
