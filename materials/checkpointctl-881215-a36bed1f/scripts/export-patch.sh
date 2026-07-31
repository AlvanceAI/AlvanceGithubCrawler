#!/usr/bin/env bash
set -euo pipefail
base_commit=a36bed1feb563fcc121917a48e780a4731f5396b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
