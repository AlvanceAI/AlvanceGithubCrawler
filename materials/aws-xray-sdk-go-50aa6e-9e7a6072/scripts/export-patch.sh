#!/usr/bin/env bash
set -euo pipefail
base_commit=9e7a607272c7a4f460e73d7b793f07b83db7e27d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
