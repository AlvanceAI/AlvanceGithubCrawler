#!/usr/bin/env bash
set -euo pipefail
base_commit=c03cbba75db1fcde54fac2210e5be9c63737076c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
