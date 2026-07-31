#!/usr/bin/env bash
set -euo pipefail
base_commit=c0472edb16891765fbc86573ea468365b7fd2197
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
