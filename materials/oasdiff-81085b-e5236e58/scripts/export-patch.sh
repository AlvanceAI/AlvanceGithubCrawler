#!/usr/bin/env bash
set -euo pipefail
base_commit=e5236e58664efabb695869f690872f6afb5b512c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
