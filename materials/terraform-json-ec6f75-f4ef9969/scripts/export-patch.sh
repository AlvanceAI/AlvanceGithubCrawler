#!/usr/bin/env bash
set -euo pipefail
base_commit=f4ef9969cba17897dc68940e97b0f3f203807630
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
