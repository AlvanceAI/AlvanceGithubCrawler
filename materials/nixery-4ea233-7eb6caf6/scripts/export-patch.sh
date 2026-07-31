#!/usr/bin/env bash
set -euo pipefail
base_commit=7eb6caf6c9de3d760351edaa9cb78debe4221dbd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
