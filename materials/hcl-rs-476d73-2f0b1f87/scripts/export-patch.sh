#!/usr/bin/env bash
set -euo pipefail
base_commit=2f0b1f87fbb43d6ebe61afe26e954a23242d5d1f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
