#!/usr/bin/env bash
set -euo pipefail
base_commit=5174d4c8358a6f06aa8056bafd14c2272dab8dd1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
