#!/usr/bin/env bash
set -euo pipefail
base_commit=00fc2909c64a7529fe49fb31b0fa8662342ebe69
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
