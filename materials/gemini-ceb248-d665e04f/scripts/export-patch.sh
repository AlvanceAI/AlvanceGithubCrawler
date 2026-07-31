#!/usr/bin/env bash
set -euo pipefail
base_commit=d665e04f508c16f381a862b86705d27beae82fd1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
