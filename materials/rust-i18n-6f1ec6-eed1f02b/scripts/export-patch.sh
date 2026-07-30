#!/usr/bin/env bash
set -euo pipefail
base_commit=eed1f02b65106f47e347d629489d95614cec132c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
