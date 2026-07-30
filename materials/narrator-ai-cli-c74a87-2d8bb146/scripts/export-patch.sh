#!/usr/bin/env bash
set -euo pipefail
base_commit=2d8bb1463058fb36f267f205994dca38b32f037d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
