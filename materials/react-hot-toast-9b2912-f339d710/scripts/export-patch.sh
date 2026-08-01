#!/usr/bin/env bash
set -euo pipefail
base_commit=f339d7105c90e64bc80ee836b987f2efe235035c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
