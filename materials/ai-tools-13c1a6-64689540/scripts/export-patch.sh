#!/usr/bin/env bash
set -euo pipefail
base_commit=64689540226112c04c153217c64f584a1d15c643
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
