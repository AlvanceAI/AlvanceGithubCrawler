#!/usr/bin/env bash
set -euo pipefail
base_commit=18cf418cb0ee5812761c7de664c796dca6ddfabb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
