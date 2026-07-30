#!/usr/bin/env bash
set -euo pipefail
base_commit=e23ce5f2be10b0c1deb2598ea42d365ddce875a6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
