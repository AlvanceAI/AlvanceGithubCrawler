#!/usr/bin/env bash
set -euo pipefail
base_commit=08dab401f7e78a3af923239fff1fcef20ab78464
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
