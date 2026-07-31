#!/usr/bin/env bash
set -euo pipefail
base_commit=4424eec59eff9a42af187e2a7a647f349e4839b5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
