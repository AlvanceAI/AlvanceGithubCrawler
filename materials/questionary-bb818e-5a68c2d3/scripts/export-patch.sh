#!/usr/bin/env bash
set -euo pipefail
base_commit=5a68c2d3e1d4ed01b9692b487349be66014db65f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
