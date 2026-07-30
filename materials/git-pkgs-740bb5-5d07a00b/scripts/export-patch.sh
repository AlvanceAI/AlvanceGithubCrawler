#!/usr/bin/env bash
set -euo pipefail
base_commit=5d07a00bace682d7eda71738e172d7a0ad7fb0b3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
