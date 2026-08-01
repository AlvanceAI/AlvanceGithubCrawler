#!/usr/bin/env bash
set -euo pipefail
base_commit=c1978d643ecce491929084e4290b35f57e4921ad
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
