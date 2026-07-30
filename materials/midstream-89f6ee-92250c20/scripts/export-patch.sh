#!/usr/bin/env bash
set -euo pipefail
base_commit=92250c20d8aa3d867fcc8cb75aeabbc95eb1a0cc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
