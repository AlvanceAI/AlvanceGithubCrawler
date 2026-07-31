#!/usr/bin/env bash
set -euo pipefail
base_commit=89571374212ff39c25a5ae5148000c1ca14afdb3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
