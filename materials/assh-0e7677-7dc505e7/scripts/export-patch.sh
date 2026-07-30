#!/usr/bin/env bash
set -euo pipefail
base_commit=7dc505e79cc2564866760b53c2a247fa3a167198
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
