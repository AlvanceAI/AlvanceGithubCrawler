#!/usr/bin/env bash
set -euo pipefail
base_commit=f42103da8b3dc38acd34c9c0b104aab5622a21a7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
