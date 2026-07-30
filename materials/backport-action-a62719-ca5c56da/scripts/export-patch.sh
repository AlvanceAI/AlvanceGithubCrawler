#!/usr/bin/env bash
set -euo pipefail
base_commit=ca5c56da5a0c130ee110184b95767d7685ceaf8e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
