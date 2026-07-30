#!/usr/bin/env bash
set -euo pipefail
base_commit=90d36ed2ae2a2e11977af748b0220f2baef60f56
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
