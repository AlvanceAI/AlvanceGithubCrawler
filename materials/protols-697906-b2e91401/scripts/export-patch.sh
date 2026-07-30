#!/usr/bin/env bash
set -euo pipefail
base_commit=b2e9140166bf9d174986c4dffc2b385d6b846f21
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
