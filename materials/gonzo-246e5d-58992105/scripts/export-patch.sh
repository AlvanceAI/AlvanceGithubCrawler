#!/usr/bin/env bash
set -euo pipefail
base_commit=5899210555ed4ecbbed493b7ca0d48436f941505
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
