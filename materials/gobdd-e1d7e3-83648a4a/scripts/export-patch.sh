#!/usr/bin/env bash
set -euo pipefail
base_commit=83648a4a49b5c506634ddd0e67c895d6d5cdbaa8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
