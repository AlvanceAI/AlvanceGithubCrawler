#!/usr/bin/env bash
set -euo pipefail
base_commit=a29287e8152456b8d6a09121934522fd2b4e0aa8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
