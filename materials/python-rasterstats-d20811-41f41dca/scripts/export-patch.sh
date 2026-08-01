#!/usr/bin/env bash
set -euo pipefail
base_commit=41f41dca4bc8e2d7ca625c4d380d6bccb607a0ea
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
