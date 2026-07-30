#!/usr/bin/env bash
set -euo pipefail
base_commit=8a24ce2e2828117f69ffc31134ed12f36d33fac4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
