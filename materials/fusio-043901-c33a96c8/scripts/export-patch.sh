#!/usr/bin/env bash
set -euo pipefail
base_commit=c33a96c8a124c17500924823658541ec1d4bbfb3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
