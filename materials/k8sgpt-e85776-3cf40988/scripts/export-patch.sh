#!/usr/bin/env bash
set -euo pipefail
base_commit=3cf409884aca02b7da6b7a0cb73d0de4c8b6437b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
