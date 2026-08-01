#!/usr/bin/env bash
set -euo pipefail
base_commit=7701ee065f50a04380f81361befd754810cb9e28
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
