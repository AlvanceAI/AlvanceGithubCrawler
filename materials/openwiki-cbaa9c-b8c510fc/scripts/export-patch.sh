#!/usr/bin/env bash
set -euo pipefail
base_commit=b8c510fce4afab5cc855390f67f833137183d646
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
