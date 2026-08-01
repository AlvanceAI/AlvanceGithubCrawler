#!/usr/bin/env bash
set -euo pipefail
base_commit=7848fbd8c9e4a08aff16e68f42cd84128f907783
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
