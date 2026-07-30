#!/usr/bin/env bash
set -euo pipefail
base_commit=a7d530442e0bbcee3b7e331ce3d1397766ddf218
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
