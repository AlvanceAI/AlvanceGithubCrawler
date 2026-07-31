#!/usr/bin/env bash
set -euo pipefail
base_commit=63a00b513979ccc96b530da2f3efb677361d573c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
