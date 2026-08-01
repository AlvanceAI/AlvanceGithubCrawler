#!/usr/bin/env bash
set -euo pipefail
base_commit=88e3d965c0b1628642a30a841745b410d6835052
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
