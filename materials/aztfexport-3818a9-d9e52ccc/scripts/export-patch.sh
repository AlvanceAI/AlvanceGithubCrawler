#!/usr/bin/env bash
set -euo pipefail
base_commit=d9e52ccc6a888175f04d50730551345cf20d92c6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
