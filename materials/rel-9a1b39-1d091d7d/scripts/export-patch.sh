#!/usr/bin/env bash
set -euo pipefail
base_commit=1d091d7ddfd47c78cb5aec13c929b2d1da37885d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
