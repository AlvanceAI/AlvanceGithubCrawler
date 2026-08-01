#!/usr/bin/env bash
set -euo pipefail
base_commit=6ad69302c8517e602e4d5ed4a2b9026a0d7bb08d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
