#!/usr/bin/env bash
set -euo pipefail
base_commit=7a30ce11dc4b27bb90a6a70ce96e21cf1872bb71
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
