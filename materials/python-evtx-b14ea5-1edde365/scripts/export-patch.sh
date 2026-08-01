#!/usr/bin/env bash
set -euo pipefail
base_commit=1edde3655c676bd44990ce9762d6b8f73334ed1d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
