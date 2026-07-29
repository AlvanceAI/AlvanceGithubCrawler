#!/usr/bin/env bash
set -euo pipefail
base_commit=20af3bdf87157bb915187085771253b1d60d298c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
