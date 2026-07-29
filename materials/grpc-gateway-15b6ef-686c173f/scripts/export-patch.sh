#!/usr/bin/env bash
set -euo pipefail
base_commit=686c173ffa8149b5e0758483b43b856dd8bc0ab7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
