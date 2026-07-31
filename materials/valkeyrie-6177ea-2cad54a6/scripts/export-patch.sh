#!/usr/bin/env bash
set -euo pipefail
base_commit=2cad54a665830cd3993e0af02f5e370e319af055
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
