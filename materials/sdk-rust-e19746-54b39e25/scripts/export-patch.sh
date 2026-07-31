#!/usr/bin/env bash
set -euo pipefail
base_commit=54b39e25e80bbbd618faeb918ed0973b2daec256
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
