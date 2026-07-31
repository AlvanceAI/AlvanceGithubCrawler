#!/usr/bin/env bash
set -euo pipefail
base_commit=3cd6d6371fc2f5fea00309cb74154254cef89947
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
