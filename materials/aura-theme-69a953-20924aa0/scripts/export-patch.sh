#!/usr/bin/env bash
set -euo pipefail
base_commit=20924aa0a43975420edd0e0b2f919e07a3eff9c9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
