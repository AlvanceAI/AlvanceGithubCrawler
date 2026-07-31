#!/usr/bin/env bash
set -euo pipefail
base_commit=111c425a8110072e7eae08266ac57df0b6f2b664
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
