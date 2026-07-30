#!/usr/bin/env bash
set -euo pipefail
base_commit=24f450b544afead1fb3070259e94d724aec5223e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
