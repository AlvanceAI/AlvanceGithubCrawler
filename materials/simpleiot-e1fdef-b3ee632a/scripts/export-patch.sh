#!/usr/bin/env bash
set -euo pipefail
base_commit=b3ee632ab1ced6a89166a02aee441a933e7e67ab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
