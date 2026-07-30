#!/usr/bin/env bash
set -euo pipefail
base_commit=933147567b62271565d9a719d30eaf42d25c6139
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
