#!/usr/bin/env bash
set -euo pipefail
base_commit=ac592b1e33bd379c97437884050e3105a4bae78e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
