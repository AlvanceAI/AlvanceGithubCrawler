#!/usr/bin/env bash
set -euo pipefail
base_commit=8c31a8f58ee6c642f0f5d6c0693ec6b637d849f8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
