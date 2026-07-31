#!/usr/bin/env bash
set -euo pipefail
base_commit=b209d4a90aee03420eed5c14d0552b56bd7f89c5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
