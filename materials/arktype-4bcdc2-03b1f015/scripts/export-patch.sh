#!/usr/bin/env bash
set -euo pipefail
base_commit=03b1f015d9b7c5af5dac2caed1aeedefaf705ab3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
