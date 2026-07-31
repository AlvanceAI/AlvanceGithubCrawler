#!/usr/bin/env bash
set -euo pipefail
base_commit=6b316b85793ed0157d5987a53f0aaecfb46eac1b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
