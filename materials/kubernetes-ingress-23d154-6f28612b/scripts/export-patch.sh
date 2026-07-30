#!/usr/bin/env bash
set -euo pipefail
base_commit=6f28612b6c0b596f7188cc4baa20f7745fe2ef6e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
