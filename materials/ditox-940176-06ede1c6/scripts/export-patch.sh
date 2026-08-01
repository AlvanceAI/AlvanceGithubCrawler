#!/usr/bin/env bash
set -euo pipefail
base_commit=06ede1c62a96fff7333558756f8f8047487c978b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
