#!/usr/bin/env bash
set -euo pipefail
base_commit=61a83eb294b80e2792d5587a0fd7dc46cafe5681
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
