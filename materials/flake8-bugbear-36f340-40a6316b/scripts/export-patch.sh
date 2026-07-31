#!/usr/bin/env bash
set -euo pipefail
base_commit=40a6316bb2018b7e4c8c243186a8f2de0721200b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
