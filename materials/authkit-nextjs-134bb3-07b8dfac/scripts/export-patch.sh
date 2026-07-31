#!/usr/bin/env bash
set -euo pipefail
base_commit=07b8dfac63321d2a5f7fdacd033d02728c099ebe
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
