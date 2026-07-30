#!/usr/bin/env bash
set -euo pipefail
base_commit=efd7aa67b36f2a623e947569c83c55aa783e1e20
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
