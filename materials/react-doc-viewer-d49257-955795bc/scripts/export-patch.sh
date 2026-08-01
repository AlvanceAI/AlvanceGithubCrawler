#!/usr/bin/env bash
set -euo pipefail
base_commit=955795bca8bb5c81f76674321a019ef4f838f307
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
