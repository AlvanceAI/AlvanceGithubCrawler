#!/usr/bin/env bash
set -euo pipefail
base_commit=2f4795fc7dcd6c7274c557eabd461be816e9b3ae
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
