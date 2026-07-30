#!/usr/bin/env bash
set -euo pipefail
base_commit=c6a0c3cebf3395635e61075d2c81a96a710d4910
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
