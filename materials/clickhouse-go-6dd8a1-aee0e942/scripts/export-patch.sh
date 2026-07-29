#!/usr/bin/env bash
set -euo pipefail
base_commit=aee0e942aa21616498a72027b3475fa271b677aa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
