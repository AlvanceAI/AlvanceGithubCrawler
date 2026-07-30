#!/usr/bin/env bash
set -euo pipefail
base_commit=734544cd88756fc65230c1b2d2b53805bfb506a9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
