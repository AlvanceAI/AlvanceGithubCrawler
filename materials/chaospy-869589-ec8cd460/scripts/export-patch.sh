#!/usr/bin/env bash
set -euo pipefail
base_commit=ec8cd460bf1440eca4b409d996cfdb104d24ae06
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
