#!/usr/bin/env bash
set -euo pipefail
base_commit=af719b43cad19d9cbad436ba10d08e413ab272d1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
