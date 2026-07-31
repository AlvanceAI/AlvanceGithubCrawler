#!/usr/bin/env bash
set -euo pipefail
base_commit=ae7c85606b38cd3f68cdd83be29be1f2a00fcb73
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
