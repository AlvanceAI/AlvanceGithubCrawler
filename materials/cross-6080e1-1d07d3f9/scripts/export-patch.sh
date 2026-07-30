#!/usr/bin/env bash
set -euo pipefail
base_commit=1d07d3f9cc465c435256f1aabc1d18024517891a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
