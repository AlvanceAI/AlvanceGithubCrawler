#!/usr/bin/env bash
set -euo pipefail
base_commit=8e7225ab187046465ff315e68fb43a7315ba561e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
