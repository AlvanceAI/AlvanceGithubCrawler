#!/usr/bin/env bash
set -euo pipefail
base_commit=24842fd5082e19126d35324f19c114f6a3328219
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
