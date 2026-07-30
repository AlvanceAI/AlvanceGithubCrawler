#!/usr/bin/env bash
set -euo pipefail
base_commit=e010ca02e0eb28daf544c0447fdd64e4e99d5c5e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
