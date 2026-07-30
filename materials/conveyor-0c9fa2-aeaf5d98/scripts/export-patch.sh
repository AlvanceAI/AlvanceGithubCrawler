#!/usr/bin/env bash
set -euo pipefail
base_commit=aeaf5d98ba49d00809b4496b43507573fef19ab8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
