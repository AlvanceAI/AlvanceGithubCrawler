#!/usr/bin/env bash
set -euo pipefail
base_commit=6e4ec41a8b1e0f41985d10aef16ea72ad58fdc72
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
