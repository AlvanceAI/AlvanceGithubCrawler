#!/usr/bin/env bash
set -euo pipefail
base_commit=4dc06b251e737dbdfc56381bcd884b97739e512e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
