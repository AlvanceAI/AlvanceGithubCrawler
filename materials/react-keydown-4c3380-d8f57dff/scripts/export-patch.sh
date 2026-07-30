#!/usr/bin/env bash
set -euo pipefail
base_commit=d8f57dff1a81aba81bc343314beb518aa8f6d23c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
