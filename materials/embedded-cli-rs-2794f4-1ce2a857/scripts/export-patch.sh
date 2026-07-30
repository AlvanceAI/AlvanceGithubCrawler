#!/usr/bin/env bash
set -euo pipefail
base_commit=1ce2a8572a3620665b22da9dbbd1c88ec8867b7f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
