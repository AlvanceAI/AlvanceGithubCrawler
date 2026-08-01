#!/usr/bin/env bash
set -euo pipefail
base_commit=b71edf0b1b80aa22a16222775fbd37dabab3aea0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
