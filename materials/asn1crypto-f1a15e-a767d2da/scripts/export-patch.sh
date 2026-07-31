#!/usr/bin/env bash
set -euo pipefail
base_commit=a767d2daa8ef4549d497b67a0304561c2eb4b858
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
