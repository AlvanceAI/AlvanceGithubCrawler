#!/usr/bin/env bash
set -euo pipefail
base_commit=0089c89c94753bebbec12b956c07a1cd38740379
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
