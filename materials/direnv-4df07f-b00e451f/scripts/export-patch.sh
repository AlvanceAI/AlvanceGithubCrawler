#!/usr/bin/env bash
set -euo pipefail
base_commit=b00e451f547f39be7ab836d969054114a465a0f9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
