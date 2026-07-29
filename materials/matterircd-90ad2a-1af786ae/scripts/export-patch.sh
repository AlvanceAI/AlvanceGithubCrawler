#!/usr/bin/env bash
set -euo pipefail
base_commit=1af786aed7b4ec4e551e1577648a728478c5aef6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
