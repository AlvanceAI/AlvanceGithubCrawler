#!/usr/bin/env bash
set -euo pipefail
base_commit=4b03c6a2f4381e2a4fd119ed2cb4e9c8d96192f2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
