#!/usr/bin/env bash
set -euo pipefail
base_commit=184e01a188a6c010079eb0dcfc4f8b6dd66a33a7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
