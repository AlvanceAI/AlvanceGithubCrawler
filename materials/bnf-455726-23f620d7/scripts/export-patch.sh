#!/usr/bin/env bash
set -euo pipefail
base_commit=23f620d76433dda9069d2d557c92341ae0cec6fd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
