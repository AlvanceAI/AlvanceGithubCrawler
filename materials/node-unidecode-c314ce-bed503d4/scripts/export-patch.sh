#!/usr/bin/env bash
set -euo pipefail
base_commit=bed503d432d3c8e4e78f1914cff0ed793fd6aecc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
