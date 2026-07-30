#!/usr/bin/env bash
set -euo pipefail
base_commit=6ee9b33f76d35f9cc7125c3c7511bce4b1e829c4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
