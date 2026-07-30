#!/usr/bin/env bash
set -euo pipefail
base_commit=b4ad84f7c5548fbab3972436e1a000fb5f829cdc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
