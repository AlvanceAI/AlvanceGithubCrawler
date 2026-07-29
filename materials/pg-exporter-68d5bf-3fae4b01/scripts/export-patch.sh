#!/usr/bin/env bash
set -euo pipefail
base_commit=3fae4b0166decd6c13372603f7455e6cb39ed9bb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
