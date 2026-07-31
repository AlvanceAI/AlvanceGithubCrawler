#!/usr/bin/env bash
set -euo pipefail
base_commit=b4c02f9d339e513fd22d756b0f37efb780c0be73
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
