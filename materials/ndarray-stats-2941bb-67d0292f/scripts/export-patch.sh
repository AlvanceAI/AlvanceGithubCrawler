#!/usr/bin/env bash
set -euo pipefail
base_commit=67d0292f483c90b8afa0c975832d979d24204e95
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
