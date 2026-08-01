#!/usr/bin/env bash
set -euo pipefail
base_commit=a47da67fcee99b79eaf7ff2af0cd359652dae312
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
