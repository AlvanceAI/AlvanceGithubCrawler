#!/usr/bin/env bash
set -euo pipefail
base_commit=d252fc626c703d0ca510e74b130bbd0cf86da6fc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
