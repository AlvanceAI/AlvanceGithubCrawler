#!/usr/bin/env bash
set -euo pipefail
base_commit=4bdf5315b6a8d05490070f07262c689d25af02e7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
