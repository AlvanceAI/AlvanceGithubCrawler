#!/usr/bin/env bash
set -euo pipefail
base_commit=2e6a8d14baf0268f4e2aa4d01784a54ca935cf52
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
