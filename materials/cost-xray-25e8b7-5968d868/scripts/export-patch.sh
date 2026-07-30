#!/usr/bin/env bash
set -euo pipefail
base_commit=5968d8689864e37fe44985b3568f10440a97989f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
