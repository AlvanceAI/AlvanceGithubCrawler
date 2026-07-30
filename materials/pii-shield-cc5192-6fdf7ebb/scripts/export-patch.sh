#!/usr/bin/env bash
set -euo pipefail
base_commit=6fdf7ebb3a88a8d2c56a0b18fbd2a52c3e5cb89b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
