#!/usr/bin/env bash
set -euo pipefail
base_commit=dfbe3fe414d0caccb76348e9e3cd9dae9943f9ad
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
