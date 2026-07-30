#!/usr/bin/env bash
set -euo pipefail
base_commit=1b9be32f47e3d63919daf2025be586b621f81e02
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
