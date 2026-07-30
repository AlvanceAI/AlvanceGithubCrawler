#!/usr/bin/env bash
set -euo pipefail
base_commit=5ae6e7a55748414b4be30a832afd895014c65352
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
