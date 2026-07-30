#!/usr/bin/env bash
set -euo pipefail
base_commit=9b9e4a4b829f22f53181c84df19915b858599bbb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
