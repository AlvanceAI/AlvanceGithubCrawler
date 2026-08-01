#!/usr/bin/env bash
set -euo pipefail
base_commit=c83bd1169ae62d761862e53b2e15a66466ea0b05
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
