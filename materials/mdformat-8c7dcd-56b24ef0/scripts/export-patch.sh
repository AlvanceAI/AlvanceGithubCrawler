#!/usr/bin/env bash
set -euo pipefail
base_commit=56b24ef0c6cfdab501844925971204f858185547
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
