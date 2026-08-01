#!/usr/bin/env bash
set -euo pipefail
base_commit=561a3d1e94705202d9ffab8297500627c1a452c9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
