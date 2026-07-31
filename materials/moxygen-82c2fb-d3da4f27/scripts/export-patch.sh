#!/usr/bin/env bash
set -euo pipefail
base_commit=d3da4f27c084a383538353c300b2bf15403b3b27
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
