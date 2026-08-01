#!/usr/bin/env bash
set -euo pipefail
base_commit=b474daf9cf1ef55e9161009cb06bb996072d0df0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
