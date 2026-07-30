#!/usr/bin/env bash
set -euo pipefail
base_commit=648fd0c4ac5f1678583c1be206c01fc3a3788efc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
