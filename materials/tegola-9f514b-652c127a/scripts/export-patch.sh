#!/usr/bin/env bash
set -euo pipefail
base_commit=652c127a057f020715e202e9dd832317a6308a77
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
