#!/usr/bin/env bash
set -euo pipefail
base_commit=d2ac1ed6832a06675db760c60d5d018013960522
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
