#!/usr/bin/env bash
set -euo pipefail
base_commit=fd04284451985cccb94c6161cd81516a654d6d37
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
