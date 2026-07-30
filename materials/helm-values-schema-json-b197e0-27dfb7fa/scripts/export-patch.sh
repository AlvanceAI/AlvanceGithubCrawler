#!/usr/bin/env bash
set -euo pipefail
base_commit=27dfb7fa5a55f67464b0622bfaedd950e566d396
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
