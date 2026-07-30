#!/usr/bin/env bash
set -euo pipefail
base_commit=fa52d81acd61876f7a8171522a74d8a049f107d1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
