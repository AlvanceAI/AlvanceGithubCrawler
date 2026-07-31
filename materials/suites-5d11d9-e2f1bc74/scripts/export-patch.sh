#!/usr/bin/env bash
set -euo pipefail
base_commit=e2f1bc74abd5d14d2817f39880d20ad52989dc1e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
