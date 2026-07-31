#!/usr/bin/env bash
set -euo pipefail
base_commit=cf1c30333df2d6b19e6208f67157024975bdba82
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
