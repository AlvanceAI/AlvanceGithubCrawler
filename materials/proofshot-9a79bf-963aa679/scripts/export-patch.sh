#!/usr/bin/env bash
set -euo pipefail
base_commit=963aa67949ad8e82810135e0a7cfce4827fd4686
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
