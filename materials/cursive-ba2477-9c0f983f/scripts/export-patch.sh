#!/usr/bin/env bash
set -euo pipefail
base_commit=9c0f983f3c691b3a818b2abe408542d3e71894d0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
