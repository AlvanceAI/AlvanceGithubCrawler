#!/usr/bin/env bash
set -euo pipefail
base_commit=7f0bb4060772e78fb52d48b73a38b8c3928e83f0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
