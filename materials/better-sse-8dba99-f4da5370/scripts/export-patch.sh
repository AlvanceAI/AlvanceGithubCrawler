#!/usr/bin/env bash
set -euo pipefail
base_commit=f4da53706d17aac70bdc31dc210688034d638445
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
