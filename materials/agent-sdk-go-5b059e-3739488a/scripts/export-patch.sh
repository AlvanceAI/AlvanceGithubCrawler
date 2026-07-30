#!/usr/bin/env bash
set -euo pipefail
base_commit=3739488a85c5671319843f61dd655c2da8fcb0ed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
