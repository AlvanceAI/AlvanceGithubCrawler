#!/usr/bin/env bash
set -euo pipefail
base_commit=5bb50c177f296d2dc45c60538929b51464aecdff
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
