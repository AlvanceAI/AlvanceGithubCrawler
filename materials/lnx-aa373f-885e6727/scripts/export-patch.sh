#!/usr/bin/env bash
set -euo pipefail
base_commit=885e6727196aa1dda9bb88fedcb45d14a9284770
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
