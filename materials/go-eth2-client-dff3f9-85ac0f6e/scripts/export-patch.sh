#!/usr/bin/env bash
set -euo pipefail
base_commit=85ac0f6e00e8230c030d9756350ea5e4acd52d2c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
