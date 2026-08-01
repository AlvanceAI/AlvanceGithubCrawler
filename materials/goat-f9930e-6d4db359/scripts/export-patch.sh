#!/usr/bin/env bash
set -euo pipefail
base_commit=6d4db359c601eae6efa1fcd94601fa1793e114d5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
