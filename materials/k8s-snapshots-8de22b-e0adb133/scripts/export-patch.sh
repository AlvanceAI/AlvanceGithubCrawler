#!/usr/bin/env bash
set -euo pipefail
base_commit=e0adb133cf2df30abb649f35c1a8cd2a1dbc9229
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
