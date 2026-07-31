#!/usr/bin/env bash
set -euo pipefail
base_commit=961ec31f576c5817ece779ff73982b4553760a4e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
