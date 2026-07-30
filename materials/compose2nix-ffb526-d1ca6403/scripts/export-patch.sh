#!/usr/bin/env bash
set -euo pipefail
base_commit=d1ca640306419bdcffca8a2e8490ccdf970706f6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
