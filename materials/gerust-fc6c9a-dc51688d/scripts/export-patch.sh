#!/usr/bin/env bash
set -euo pipefail
base_commit=dc51688dc87770e15cd634379f9e9118d15637ed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
