#!/usr/bin/env bash
set -euo pipefail
base_commit=fb196956b1853752ed7fe13d3dd4572c45c16709
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
