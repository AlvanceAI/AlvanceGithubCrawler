#!/usr/bin/env bash
set -euo pipefail
base_commit=db52e28f4d9ded852ab3942cea316258ae4ef346
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
