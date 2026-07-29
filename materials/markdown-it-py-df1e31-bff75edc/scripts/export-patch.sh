#!/usr/bin/env bash
set -euo pipefail
base_commit=bff75edcd7e6ce68f417803361d6e9f1223ad373
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
