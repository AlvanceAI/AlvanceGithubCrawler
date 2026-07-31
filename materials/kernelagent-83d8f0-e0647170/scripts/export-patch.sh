#!/usr/bin/env bash
set -euo pipefail
base_commit=e0647170da36ef9b059ac0bd3d60103aa4ed378b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
