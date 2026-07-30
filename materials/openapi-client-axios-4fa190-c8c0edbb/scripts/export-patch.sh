#!/usr/bin/env bash
set -euo pipefail
base_commit=c8c0edbbd655fbfe5b2408f49949e95d17d13c47
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
