#!/usr/bin/env bash
set -euo pipefail
base_commit=48af73ca62aaa54c4ec3a086739486efdc9733aa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
