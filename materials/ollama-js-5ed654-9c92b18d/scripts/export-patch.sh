#!/usr/bin/env bash
set -euo pipefail
base_commit=9c92b18d4026f5345ff7950f15216372b23401a1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
