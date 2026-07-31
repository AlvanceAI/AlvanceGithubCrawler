#!/usr/bin/env bash
set -euo pipefail
base_commit=efcb1a3629f60b5e0bec21c1f2a74c19bd2210f5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
