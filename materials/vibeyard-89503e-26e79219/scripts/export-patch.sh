#!/usr/bin/env bash
set -euo pipefail
base_commit=26e79219539ea8b830334d03d4be890fb7ba062b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
