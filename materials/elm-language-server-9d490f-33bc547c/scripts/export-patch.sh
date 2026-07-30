#!/usr/bin/env bash
set -euo pipefail
base_commit=33bc547c259a195e613069d364aae2af88e63432
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
