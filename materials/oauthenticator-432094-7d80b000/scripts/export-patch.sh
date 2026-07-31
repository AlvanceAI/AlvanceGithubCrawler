#!/usr/bin/env bash
set -euo pipefail
base_commit=7d80b0000d8b11e639f3fe0f63d0711e057a15df
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
