#!/usr/bin/env bash
set -euo pipefail
base_commit=e5516da3feb31c03024571ad8ea674804f121922
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
