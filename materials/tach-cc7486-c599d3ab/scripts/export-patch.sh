#!/usr/bin/env bash
set -euo pipefail
base_commit=c599d3ab87361f0d458f286b00a8d8913e2fce8d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
