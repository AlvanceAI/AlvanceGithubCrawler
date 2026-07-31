#!/usr/bin/env bash
set -euo pipefail
base_commit=46385c500f47267607a2cdde63feef59247615f5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
