#!/usr/bin/env bash
set -euo pipefail
base_commit=b3ebf2a00618bf200be09cb04f5b2b9414eb1d15
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
