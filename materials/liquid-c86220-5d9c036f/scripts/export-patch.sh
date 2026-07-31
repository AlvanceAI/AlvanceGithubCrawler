#!/usr/bin/env bash
set -euo pipefail
base_commit=5d9c036f526eb1b07e83e33beb6047329d2e7004
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
