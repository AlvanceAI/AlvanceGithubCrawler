#!/usr/bin/env bash
set -euo pipefail
base_commit=9deb6a2cf20e17aa15dc3fb735768b6b86d3a991
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
