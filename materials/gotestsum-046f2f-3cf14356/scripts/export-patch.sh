#!/usr/bin/env bash
set -euo pipefail
base_commit=3cf14356a16c7931cfeacd7dfee585527618df3d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
