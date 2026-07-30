#!/usr/bin/env bash
set -euo pipefail
base_commit=5cfe17e9b3c69aee6e65cc5d73b7c40cc1ffa87e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
