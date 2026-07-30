#!/usr/bin/env bash
set -euo pipefail
base_commit=4a4ca0454974f2548fc7ad683c502bacfe873f6e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
