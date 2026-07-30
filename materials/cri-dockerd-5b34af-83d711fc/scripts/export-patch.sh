#!/usr/bin/env bash
set -euo pipefail
base_commit=83d711fce4f8d6803138020da3faac2d81108173
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
