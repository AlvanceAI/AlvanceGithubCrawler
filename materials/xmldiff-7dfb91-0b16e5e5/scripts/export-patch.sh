#!/usr/bin/env bash
set -euo pipefail
base_commit=0b16e5e52fcf189fb489ed83bd1ed306506e509b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
