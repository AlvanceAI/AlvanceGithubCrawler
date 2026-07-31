#!/usr/bin/env bash
set -euo pipefail
base_commit=b1f333e226f40935be83ee3977500b2f49cff563
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
