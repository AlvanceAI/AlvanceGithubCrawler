#!/usr/bin/env bash
set -euo pipefail
base_commit=04d3b87cbc1db020d28c7cfb44fe194558efbdde
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
