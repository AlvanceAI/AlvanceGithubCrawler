#!/usr/bin/env bash
set -euo pipefail
base_commit=6e4cd893c1d21befe7deebe03e93e8a1d95248c8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
