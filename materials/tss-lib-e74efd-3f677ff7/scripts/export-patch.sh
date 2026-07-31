#!/usr/bin/env bash
set -euo pipefail
base_commit=3f677ff761fcf692edb0243a5d812930844d879a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
