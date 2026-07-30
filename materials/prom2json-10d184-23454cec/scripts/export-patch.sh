#!/usr/bin/env bash
set -euo pipefail
base_commit=23454cec4175a4a3c877b8ed4c11631555387f8f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
