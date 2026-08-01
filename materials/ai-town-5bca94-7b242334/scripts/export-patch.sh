#!/usr/bin/env bash
set -euo pipefail
base_commit=7b242334bfbfef02f7718bded120d431e8f307df
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
