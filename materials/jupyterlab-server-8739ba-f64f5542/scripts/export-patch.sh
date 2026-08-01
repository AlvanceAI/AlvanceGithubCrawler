#!/usr/bin/env bash
set -euo pipefail
base_commit=f64f554291a09f072e479ff52ae2212084aaac39
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
