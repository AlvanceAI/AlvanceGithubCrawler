#!/usr/bin/env bash
set -euo pipefail
base_commit=a283527c7939b021b8baba26a3c8543db19f6318
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
