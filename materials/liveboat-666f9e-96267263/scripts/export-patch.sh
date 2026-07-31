#!/usr/bin/env bash
set -euo pipefail
base_commit=9626726306f5c5138dc34bfeea336412a1c589ee
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
