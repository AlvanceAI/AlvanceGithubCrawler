#!/usr/bin/env bash
set -euo pipefail
base_commit=9b269c4375e9ab56bc47df0e4a1109c746d3db81
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
