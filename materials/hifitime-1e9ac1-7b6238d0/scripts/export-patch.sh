#!/usr/bin/env bash
set -euo pipefail
base_commit=7b6238d0bfdfee940dca49e217f3a59c9234e6ab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
