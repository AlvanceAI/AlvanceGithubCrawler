#!/usr/bin/env bash
set -euo pipefail
base_commit=a0219204842978493e5f7742b0c06d5c39951e73
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
