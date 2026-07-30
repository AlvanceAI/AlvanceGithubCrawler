#!/usr/bin/env bash
set -euo pipefail
base_commit=3997ef66d0ca3b9e4099e33e1014cfa03029898f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
