#!/usr/bin/env bash
set -euo pipefail
base_commit=b381c400d4db4d6058d7579addf04a0b9825e941
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
