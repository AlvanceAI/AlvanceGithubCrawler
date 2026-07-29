#!/usr/bin/env bash
set -euo pipefail
base_commit=cde0999907e7f49df3e4af031545a9348b0cccdd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
