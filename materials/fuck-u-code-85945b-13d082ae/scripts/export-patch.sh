#!/usr/bin/env bash
set -euo pipefail
base_commit=13d082ae744cfeb45185460572b8033b08c4a37c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
