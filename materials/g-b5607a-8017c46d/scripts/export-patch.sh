#!/usr/bin/env bash
set -euo pipefail
base_commit=8017c46d7f61d6286254561e877a5bc907805b63
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
