#!/usr/bin/env bash
set -euo pipefail
base_commit=8681ca499df68da0b77122a8d55c4c679bf837de
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
