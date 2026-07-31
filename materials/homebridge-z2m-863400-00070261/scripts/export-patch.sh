#!/usr/bin/env bash
set -euo pipefail
base_commit=000702614933a6d307d0208f559b35af6b397eee
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
