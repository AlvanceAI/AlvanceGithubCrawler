#!/usr/bin/env bash
set -euo pipefail
base_commit=ab97afde87261552b70599561852df1d62d92aff
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
