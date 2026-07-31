#!/usr/bin/env bash
set -euo pipefail
base_commit=35ea7d19fda83ad132190c419215862c3d1ad091
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
