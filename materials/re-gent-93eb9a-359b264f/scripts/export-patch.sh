#!/usr/bin/env bash
set -euo pipefail
base_commit=359b264fa3bb804dbdf42ea792c759434873d325
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
