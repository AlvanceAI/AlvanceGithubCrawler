#!/usr/bin/env bash
set -euo pipefail
base_commit=5e27e1058b49d0ab28d5a72fe03ddef5a1da05a0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
