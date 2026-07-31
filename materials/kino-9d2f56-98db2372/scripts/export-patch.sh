#!/usr/bin/env bash
set -euo pipefail
base_commit=98db23720a823fcd1f7267cbadea6304be900edc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
