#!/usr/bin/env bash
set -euo pipefail
base_commit=0c6c12523fc2d2f773630ec3e7ce772d23b70bbb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
