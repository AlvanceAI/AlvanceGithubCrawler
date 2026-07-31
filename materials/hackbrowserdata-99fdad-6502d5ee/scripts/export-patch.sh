#!/usr/bin/env bash
set -euo pipefail
base_commit=6502d5ee14a4e1c84e4b027bac86369ea9475f46
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
