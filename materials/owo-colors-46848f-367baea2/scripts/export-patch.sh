#!/usr/bin/env bash
set -euo pipefail
base_commit=367baea2456f01d5a9b793eaf4b5217184c5d099
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
