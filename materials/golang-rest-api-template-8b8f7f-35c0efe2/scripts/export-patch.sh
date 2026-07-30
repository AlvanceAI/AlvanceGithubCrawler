#!/usr/bin/env bash
set -euo pipefail
base_commit=35c0efe2609c3877124b4a19c8411e28648a077b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
