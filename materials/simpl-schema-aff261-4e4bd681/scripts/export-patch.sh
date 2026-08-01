#!/usr/bin/env bash
set -euo pipefail
base_commit=4e4bd6816a897267f92160a33a5f99a21c22e501
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
